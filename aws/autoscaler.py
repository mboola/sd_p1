import pika
import math
import time
import signal
import threading
import boto3
import graph as generate_graph

# RabbitMQ queue names
INSULT_QUEUE = "insult_queue"
TEXT_QUEUE = "text_queue"

# Limits so lambdas do not get out of control
MAX_NODES = 4
MIN_NODES = 1
SCALE_INTERVAL = 1

# Lambdas running
INSULT_NODE = "lambda_insult_service"
FILTER_NODE = ""
END_PETITION_QUEUE = "end_petition_queue_"
LAMBDA_PULSE_INTERVAL = 30

# Current number of lambdas each service has deployed
current_insult_nodes = 0
current_filter_nodes = 0

# Data storage
insult_service_backlog = []
insult_service_current_nodes = []
insult_service_desired_nodes = []

insult_filter_service_backlog = []
insult_filter_service_current_nodes = []
insult_filter_service_desired_nodes = []

# Parameters for autoscaling
insult_arrival_rate = 1
filter_arrival_rate = 1
INSULT_CAPACITY = 500
INSULT_AVERAGE_TIME = 0.002
TEXT_CAPACITY = 130
TEXT_AVERAGE_TIME = 0.0067

def dynamic_scaling_insult():
	backlog = get_queue_backlog(INSULT_QUEUE)

	insult_service_backlog.append(backlog)
	insult_service_current_nodes.append(current_insult_nodes)

	desired_nodes = max(1, math.ceil((backlog + insult_arrival_rate * INSULT_AVERAGE_TIME) / INSULT_CAPACITY))
	insult_service_desired_nodes.append(desired_nodes)

	if desired_nodes > MAX_NODES:
		return MAX_NODES
	return desired_nodes

def dynamic_scaling_filter():
	backlog = get_queue_backlog(TEXT_QUEUE)

	insult_filter_service_backlog.append(backlog)
	insult_filter_service_current_nodes.append(current_filter_nodes)

	desired_nodes = max(1, math.ceil((backlog + filter_arrival_rate * TEXT_AVERAGE_TIME) / TEXT_CAPACITY))
	insult_filter_service_desired_nodes.append(desired_nodes)
	
	if desired_nodes > MAX_NODES:
		return MAX_NODES
	return desired_nodes

def create_graphs(signum, frame):
	generate_graph(insult_service_backlog, insult_service_current_nodes, insult_service_desired_nodes, "graphs/insult_service")
	generate_graph(insult_filter_service_backlog, insult_filter_service_current_nodes, insult_filter_service_desired_nodes, "graphs/insult_filter_service")

# With ctrl+Z from terminal a graph gets generated
signal.signal(signal.SIGTSTP, create_graphs)

def get_queue_backlog(queue_name):
	try:
		# Connect to RabbitMQ server
		credentials = pika.PlainCredentials('user', 'password123')
		parameters = pika.ConnectionParameters("localhost", credentials)
		connection = pika.BlockingConnection(parameters)
		channel = connection.channel()

		queue = channel.queue_declare(queue=queue_name, passive=True)
		count = queue.method.message_count
		connection.close()
		return count
	
	except Exception as e:
		print(f"[ERROR] No se pudo consultar la cola {queue_name}: {e}")
		return -1

def calculate_arrival_rate():
	global insult_arrival_rate, filter_arrival_rate
	insult_backlog = get_queue_backlog(INSULT_QUEUE)
	filter_backlog = get_queue_backlog(TEXT_QUEUE)
	while True:
		time.sleep(1) # wait 1 sec
		last_insult_backlog = insult_backlog
		insult_backlog = get_queue_backlog(INSULT_QUEUE)
		insult_arrival_rate = insult_backlog - last_insult_backlog

		last_filter_backlog = filter_backlog
		filter_backlog = get_queue_backlog(INSULT_QUEUE)
		filter_arrival_rate = filter_backlog - last_filter_backlog

# Thread that calculates the arrivar rate of both services queues
threading.Thread(target=calculate_arrival_rate, daemon=True).start()

# Function used to deploy lambdas
def scale_up(service_type, current_nodes):

	if current_nodes >= MAX_NODES:
		return MAX_NODES

	lambda_client = boto3.client('lambda', region_name='us_east-1')
	try:
		response = lambda_client.invoke(
			FunctionName=service_type,
			InvocationType='Event',
			Payload=json.dumps({"param1": current_nodes}),
		)
		return current_nodes + 1
	except Exception as e:
		print("Error invoking Lambda", e)
		return current_nodes
	
# Function used to 'kill' (notice) lambdas
def scale_down(service_type, current_nodes):

	if current_nodes <= MIN_NODES:
		return MIN_NODES
	
	queue = END_PETITION_QUEUE + str(current_nodes)

	# Notice struct[current_nodes] that lambda needs to die
	credentials = pika.PlainCredentials('user', 'password123')
	parameters = pika.ConnectionParameters("localhost", credentials)
	connection = pika.BlockingConnection(parameters)

	channel = connection.channel()
    channel.queue_declare(queue=queue, durable=True)
	channel.basic_publish(
		exchange='',
		routing_key=queue,
		body="end"
	)
	return current_nodes - 1 

# TODO: implement this
# For now this will be ignored
def lambdas_lifesupport():
	while True:
		time.sleep(LAMBDA_PULSE_INTERVAL)
		#for i in range(current_insult_nodes):
			# Here we check if there has been a pulse

		#for i in range(current_filter_nodes):


# Thread that checks if all lambdas that should be deployed are deployed.
# If they are not, it deploys them again
threading.Thread(target=lambdas_lifesupport, daemon=True).start()

# Start always a lambda with a service of each type
current_insult_nodes = scale_up(INSULT_NODE, current_insult_nodes)
current_filter_nodes = scale_up(FILTER_NODE, current_filter_nodes)

while True:
	desired_insult_nodes = dynamic_scaling_insult()
	if desired_insult_nodes > current_insult_nodes:
		nodes_dif = desired_insult_nodes - current_insult_nodes
		for i in range(nodes_dif):
			current_insult_nodes = scale_up(INSULT_NODE, current_insult_nodes)
	elif desired_insult_nodes < current_insult_nodes:
		nodes_dif = current_insult_nodes - desired_insult_nodes
		for i in range(nodes_dif):
			current_insult_nodes = scale_down(INSULT_NODE, current_insult_nodes)

	desired_filter_nodes = dynamic_scaling_filter()
	if desired_filter_nodes > current_filter_nodes:
		nodes_dif = desired_filter_nodes - current_filter_nodes
		for i in range(nodes_dif):
			current_filter_nodes = scale_up(FILTER_NODE, current_filter_nodes)
	elif desired_filter_nodes < current_filter_nodes:
		nodes_dif = current_filter_nodes - desired_filter_nodes
		for i in range(nodes_dif):
			current_filter_nodes = scale_down(FILTER_NODE, current_filter_nodes)

	time.sleep(SCALE_INTERVAL)
