import subprocess
import time
import pika
import signal
import sys
import os
import math
import threading

# Configuraciones
INSULT_QUEUE = "insult_queue"
TEXT_QUEUE = "text_queue"
INSULT_NODE = "InsultService"
FILTER_NODE = "InsultFilterService"
INSULT_PORT_BASE = 49152
TEXT_PORT_BASE = 50152

MAX_NODES = 16
MIN_NODES = 1
SCALE_INTERVAL = 5  # segundos
SCALE_UP_THRESHOLD = 300
SCALE_DOWN_THRESHOLD = 10

running_insult_nodes = []  # lista de procesos (Popen)
running_filter_nodes = []

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
INSULT_CAPACITY = 487.80
INSULT_AVERAGE_TIME = 0.00205

def dynamic_scaling_insult():
	backlog = get_queue_backlog(INSULT_QUEUE)
	print(f"Backlog: {backlog}, insult rate: {insult_arrival_rate}")
	return max(1, math.ceil((backlog + insult_arrival_rate * INSULT_AVERAGE_TIME) / INSULT_CAPACITY))

def dynamic_scaling_filter():
	filter_average_time = 1 # TODO : get filter_average_time
	filter_capacity = 1 / filter_average_time
	return max(1, math.ceil((get_queue_backlog(TEXT_QUEUE) + filter_arrival_rate * filter_average_time) / filter_capacity))

# TODO : also calculate filter gamma
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
current_insult_nodes = 1
current_filter_nodes = 1
scale_up(INSULT_NODE, running_insult_nodes, INSULT_PORT_BASE)
scale_up(FILTER_NODE, running_filter_nodes, TEXT_PORT_BASE)

while True:
	insult_nodes = dynamic_scaling_insult()
	print (f"Insult nodes: {insult_nodes} decided by dynamic scaling, and {current_insult_nodes}")

	if insult_nodes > current_insult_nodes:
		for i in range(insult_nodes - current_insult_nodes):
			scale_up(INSULT_NODE, running_insult_nodes, INSULT_PORT_BASE)
	elif insult_nodes < current_insult_nodes:
		for i in range(current_insult_nodes - insult_nodes):
			scale_down(INSULT_NODE, running_insult_nodes)
	current_insult_nodes = insult_nodes

	filter_nodes = dynamic_scaling_filter()
	print (f"Insult nodes: {filter_nodes} decided by dynamic scaling, and {current_filter_nodes}")

	if filter_nodes > current_filter_nodes:
		for i in range(filter_nodes - current_filter_nodes):
			scale_up(INSULT_NODE, running_filter_nodes, INSULT_PORT_BASE)
	elif filter_nodes < current_filter_nodes:
		for i in range(current_filter_nodes - filter_nodes):
			scale_down(INSULT_NODE, running_filter_nodes)
	current_filter_nodes = filter_nodes

	time.sleep(SCALE_INTERVAL)
