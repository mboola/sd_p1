import subprocess
import time
import pika
import signal
import sys
import os

# Configuraciones
INSULT_QUEUE = "insult_queue"
TEXT_QUEUE = "text_queue"
INSULT_NODE = "InsultService"
FILTER_NODE = "InsultFilterService"
INSULT_PORT_BASE = 49152
TEXT_PORT_BASE = 50152

MAX_NODES = 6
MIN_NODES = 1
SCALE_INTERVAL = 5  # segundos
SCALE_UP_THRESHOLD = 300
SCALE_DOWN_THRESHOLD = 10

running_insult_nodes = []  # lista de procesos (Popen)
running_text_nodes = []

def cleanup(signum, frame):
	print(f"Received signal {signum}. Cleaning up child processes...")
	for child in running_insult_nodes:
		try:
			child.terminate()
			child.wait(timeout=5)
		except Exception as e:
			print(f"Failed to terminate child: {e}")
		
	for child in running_text_nodes:
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
		print(f"[ERROR] No se pudo consultar la cola {queue_name}: {e}")
		return -1

# Function used to scale up nodes
def scale_up(service_type, node_list, base_port):
	print("what is happening")
	current_nodes = len(node_list)

	print(f"Current nodes in {service_type} is {current_nodes}")

	if current_nodes >= MAX_NODES:
		return
	
	port = base_port + current_nodes
	name = f"{service_type}_{current_nodes}"
	print(f"[UP] Lanzando {name}")
	p = subprocess.Popen(['python3', f"{service_type}/server.py", f"{port}", f"{name}"])
	node_list.append(p)

# Function used to scale down nodes
def scale_down(service_type, node_list):
	if len(node_list) > MIN_NODES:
		pid = node_list.pop()
		print(f"[DOWN] trying to kill {pid}")

		os.killpg(pid.p, signal.SIGTERM)
		print(f"[DOWN] {service_type} eliminado")

# arranca con un nodo de cada tipo
scale_up(INSULT_NODE, running_insult_nodes, INSULT_PORT_BASE)
scale_up(FILTER_NODE, running_text_nodes, TEXT_PORT_BASE)

while True:
	insult_backlog = get_queue_backlog(INSULT_QUEUE)
	text_backlog = get_queue_backlog(TEXT_QUEUE)

	print(f"Number of insults: {insult_backlog}")

	#print(f"[INFO] insult_queue: {insult_backlog}, text_queue: {text_backlog}")

	if insult_backlog > SCALE_UP_THRESHOLD:
		scale_up(INSULT_NODE, running_insult_nodes, INSULT_PORT_BASE)
	elif insult_backlog < SCALE_DOWN_THRESHOLD:
		scale_down(INSULT_NODE, running_insult_nodes)

	if text_backlog > SCALE_UP_THRESHOLD:
		scale_up(FILTER_NODE, running_text_nodes, TEXT_PORT_BASE)
	elif text_backlog < SCALE_DOWN_THRESHOLD:
		scale_down(FILTER_NODE, running_text_nodes)

	time.sleep(SCALE_INTERVAL)

