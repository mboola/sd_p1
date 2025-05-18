import subprocess
import time
import pika
import signal
import sys
import os
import math
import threading
import matplotlib.pyplot as plt

# Configuraciones
INSULT_QUEUE = "insult_queue"
TEXT_QUEUE = "text_queue"
INSULT_NODE = "InsultService"
FILTER_NODE = "InsultFilterService"
INSULT_PORT_BASE = 49152
TEXT_PORT_BASE = 50152

MAX_NODES = 16
MIN_NODES = 1
SCALE_INTERVAL = 1  # segundos

# Structs used to store values to generate graph
insult_service_backlog = []
insult_service_current_nodes = []
insult_service_desired_nodes = []

insult_filter_service_backlog = []
insult_filter_service_current_nodes = []
insult_filter_service_desired_nodes = []

current_insult_nodes = 1
current_filter_nodes = 1

running_insult_nodes = []  # lista de procesos (Popen)
running_filter_nodes = []

def generate_graph(backlog, current_nodes, desired_nodes, name_file):
	time = [i * 5 for i in range(len(backlog))]

	# Create the figure and axis objects
	fig, ax1 = plt.subplots(figsize=(10, 6))

	# Plotting current_petitions on the left y-axis
	line1, = ax1.plot(time, backlog, 'g-', label='Current Petitions')
	ax1.set_xlabel('Time (seconds)')
	ax1.set_ylabel('Current Petitions', color='g')
	ax1.tick_params(axis='y', labelcolor='g')

	ax2 = ax1.twinx()
	line2, = ax2.plot(time, current_nodes, 'b-', label='Current Nodes')
	ax2.set_ylabel('Nodes', color='b')
	ax2.tick_params(axis='y', labelcolor='b')

	ax2.set_ylim(0, 32)

	ax3 = ax1.twinx()
	ax3.spines['right'].set_position(('outward', 60))  # offset in pixels
	line3, = ax3.plot(time, desired_nodes, 'r--', label='Theoretical Nodes')
	ax3.set_ylabel('Theoretical Nodes', color='r')
	ax3.tick_params(axis='y', labelcolor='r')

	lines = [line1, line2, line3]
	labels = [line.get_label() for line in lines]
	ax1.legend(lines, labels, loc='upper left')

	# Add a title and grid
	plt.title('Autoscaler Overview: Petitions and Nodes over Time')
	ax1.grid(True)

	# Improve layout
	fig.tight_layout()

	plt.savefig(name_file, dpi=300)  # Change filename/format as needed


def cleanup(signum, frame):
	print(f"Received signal {signum}. Cleaning up child processes...")
	for child in running_insult_nodes:
		try:
			child.terminate()
			child.wait(timeout=5)
		except Exception as e:
			print(f"Failed to terminate child: {e}")
		
	for child in running_filter_nodes:
		try:
			child.terminate()
			child.wait(timeout=5)
		except Exception as e:
			print(f"Failed to terminate child: {e}")

	generate_graph(insult_service_backlog, insult_service_current_nodes, insult_service_desired_nodes, "graphs/insult_service")
	generate_graph(insult_filter_service_backlog, insult_filter_service_current_nodes, insult_filter_service_desired_nodes, "graphs/insult_filter_service")
	sys.exit(0)
    
signal.signal(signal.SIGINT, cleanup)  # Optional: handle Ctrl+C too

def get_queue_backlog(queue_name):
	try:
		# Connect to RabbitMQ server
		#credentials = pika.PlainCredentials("ar", "sar")
		parameters = pika.ConnectionParameters("localhost")
		connection = pika.BlockingConnection(parameters)
		channel = connection.channel()

		queue = channel.queue_declare(queue=queue_name, passive=True)
		count = queue.method.message_count
		connection.close()
		return count
	
	except Exception as e:
		#print(f"[ERROR] No se pudo consultar la cola {queue_name}: {e}")
		return -1

# Function used to scale up nodes
def scale_up(service_type, node_list, base_port):
	current_nodes = len(node_list)

	print(f"Current nodes in {service_type} is {current_nodes}")

	if current_nodes >= MAX_NODES:
		return
	
	port = base_port + current_nodes
	name = f"{service_type}_{current_nodes}"
	print(f"[UP] Lanzando {name}")
	p = subprocess.Popen(
		['python3', f"{service_type}/server.py", f"{port}", f"{name}"],
		preexec_fn = os.setsid)
	node_list.append(p)

# Function used to scale down nodes
def scale_down(service_type, node_list):
	if len(node_list) > MIN_NODES:
		p = node_list.pop()
		print(f"[DOWN] trying to kill {p.pid}")

		os.killpg(p.pid, signal.SIGTERM)
		print(f"[DOWN] {service_type} eliminado")

insult_arrival_rate = 1
filter_arrival_rate = 1
INSULT_CAPACITY = 500
INSULT_AVERAGE_TIME = 0.002
TEXT_CAPACITY = 130
TEXT_AVERAGE_TIME = 0.0067

def dynamic_scaling_insult():
	backlog = get_queue_backlog(INSULT_QUEUE)

	# add backlog, suposed number of nodes to deploy and current number of nodes deployed
	# into an array and each position is a SCALE_INTERVAL

	insult_service_backlog.append(backlog)
	insult_service_current_nodes.append(current_insult_nodes)

	#print(f"Backlog: {backlog}, insult rate: {insult_arrival_rate}")
	desired_nodes = max(1, math.ceil((backlog + insult_arrival_rate * INSULT_AVERAGE_TIME) / INSULT_CAPACITY))
	insult_service_desired_nodes.append(desired_nodes)

	return desired_nodes

def dynamic_scaling_filter():
	backlog = get_queue_backlog(TEXT_QUEUE)

	# add backlog, suposed number of nodes to deploy and current number of nodes deployed
	# into an array and each position is a SCALE_INTERVAL

	insult_filter_service_backlog.append(backlog)
	insult_filter_service_current_nodes.append(current_filter_nodes)

	desired_nodes = max(1, math.ceil((backlog + filter_arrival_rate * TEXT_AVERAGE_TIME) / TEXT_CAPACITY))
	insult_filter_service_desired_nodes.append(desired_nodes)

	return desired_nodes

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

# Start thread to calculate gamma
threading.Thread(target=calculate_arrival_rate, daemon=True).start()

# arranca con un nodo de cada tipo
scale_up(INSULT_NODE, running_insult_nodes, INSULT_PORT_BASE)
scale_up(FILTER_NODE, running_filter_nodes, TEXT_PORT_BASE)

while True:
	desired_insult_nodes = dynamic_scaling_insult()
	print (f"Insult nodes: {desired_insult_nodes} decided by dynamic scaling, and {current_insult_nodes}")

	if desired_insult_nodes > MAX_NODES:
		desired_insult_nodes = MAX_NODES
	
	if desired_insult_nodes > current_insult_nodes:
		for i in range(desired_insult_nodes - current_insult_nodes):
			scale_up(INSULT_NODE, running_insult_nodes, INSULT_PORT_BASE)
	elif desired_insult_nodes < current_insult_nodes:
		for i in range(current_insult_nodes - desired_insult_nodes):
			scale_down(INSULT_NODE, running_insult_nodes)

	current_insult_nodes = desired_insult_nodes

	desired_filter_nodes = dynamic_scaling_filter()
	print (f"Filter nodes: {desired_filter_nodes} decided by dynamic scaling, and {current_filter_nodes}")

	if desired_filter_nodes > MAX_NODES:
		desired_filter_nodes = MAX_NODES

	if desired_filter_nodes > current_filter_nodes:
		for i in range(desired_filter_nodes - current_filter_nodes):
			scale_up(INSULT_NODE, running_filter_nodes, INSULT_PORT_BASE)
	elif desired_filter_nodes < current_filter_nodes:
		for i in range(current_filter_nodes - desired_filter_nodes):
			scale_down(INSULT_NODE, running_filter_nodes)
	
	current_filter_nodes = desired_filter_nodes

	time.sleep(SCALE_INTERVAL)
