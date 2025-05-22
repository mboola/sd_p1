import pika
import time
import signal
import threading
import boto3
import json
import math
import graph

# RabbitMQ queue names
TEXT_QUEUE = "text_queue"

# Limits so lambdas do not get out of control
MAX_NODES = 8
MIN_NODES = 1
SCALE_INTERVAL = 10

# Lambdas running
FILTER_NODE = "lambda_filter_service"

# Current number of lambdas each service has deployed
current_filter_nodes = 0

# Data storage
insult_filter_service_backlog = []
insult_filter_service_current_nodes = []
insult_filter_service_desired_nodes = []

def dynamic_scaling_filter():
	backlog = get_queue_backlog(TEXT_QUEUE)

	insult_filter_service_backlog.append(backlog)
	insult_filter_service_current_nodes.append(current_filter_nodes)

	if current_filter_nodes <= 0:
		desired_nodes = 0
	else:
		desired_nodes = math.ceil(backlog / (current_filter_nodes * 50))
	insult_filter_service_desired_nodes.append(desired_nodes)
	
	if desired_nodes > MAX_NODES:
		return MAX_NODES
	return desired_nodes

def create_graphs(signum, frame):
	graph.generate_graph(insult_filter_service_backlog, insult_filter_service_current_nodes, insult_filter_service_desired_nodes, "graphs/insult_filter_service")

# With ctrl+Z from terminal a graph gets generated
signal.signal(signal.SIGTSTP, create_graphs)

def create_connection():
	credentials = pika.PlainCredentials('user', 'password123')
	return pika.BlockingConnection(
		pika.ConnectionParameters(
			host="localhost",
			credentials=credentials
		)
	)

def get_queue_backlog(queue_name):
	try:
		# Connect to RabbitMQ server
		connection = create_connection()
		channel = connection.channel()

		queue = channel.queue_declare(queue=queue_name, passive=True)
		count = queue.method.message_count
		connection.close()
		return count
	
	except Exception as e:
		print(f"[ERROR] No se pudo consultar la cola {queue_name}: {e}")
		return -1

def calculate_arrival_rate():
	global filter_arrival_rate
	filter_backlog = get_queue_backlog(TEXT_QUEUE)
	while True:
		time.sleep(1) # wait 1 sec
		last_filter_backlog = filter_backlog
		filter_backlog = get_queue_backlog(TEXT_QUEUE)
		filter_arrival_rate = filter_backlog - last_filter_backlog

# Thread that calculates the arrivar rate of both services queues
threading.Thread(target=calculate_arrival_rate, daemon=True).start()

# Function used to deploy lambdas
def scale_up(service_type, current_nodes):

	if current_nodes >= MAX_NODES:
		return MAX_NODES

	lambda_client = boto3.client('lambda', region_name='us-east-1')
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

while True:
	desired_filter_nodes = dynamic_scaling_filter()
	if desired_filter_nodes > current_filter_nodes:
		nodes_dif = desired_filter_nodes - current_filter_nodes
		for i in range(nodes_dif):
			current_filter_nodes = scale_up(FILTER_NODE, current_filter_nodes)
	elif desired_filter_nodes < current_filter_nodes:
		current_filter_nodes = desired_filter_nodes

	time.sleep(SCALE_INTERVAL)
