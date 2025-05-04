import subprocess
import time
import pika
import os

# Configuraciones
INSULT_QUEUE = "insult_queue"
TEXT_QUEUE = "text_queue"
INSULT_PORT_BASE = 49152
TEXT_PORT_BASE = 50152

MAX_NODES = 6
MIN_NODES = 1
SCALE_INTERVAL = 15  # segundos
SCALE_UP_THRESHOLD = 300
SCALE_DOWN_THRESHOLD = 10

running_insult_nodes = []  # lista de procesos (Popen)
running_text_nodes = []

def get_queue_backlog(queue_name):
    try:
        credentials = pika.PlainCredentials("ar", "sar")
        parameters = pika.ConnectionParameters("localhost", credentials=credentials)
        connection = pika.BlockingConnection(parameters)
        channel = connection.channel()
        queue = channel.queue_declare(queue=queue_name, passive=True)
        count = queue.method.message_count
        connection.close()
        return count
    except Exception as e:
        print(f"[ERROR] No se pudo consultar la cola {queue_name}: {e}")
        return -1

def scale_up(service_type):
    if service_type == "insult":
        i = len(running_insult_nodes)
        if i >= MAX_NODES:
            return
        port = INSULT_PORT_BASE + i
        name = f"InsultService_{i}"
        cmd = f"python3 InsultService/server.py {port} {name}"
        print(f"[UP] Lanzando {name}")
        p = subprocess.Popen(cmd, shell=True)
        running_insult_nodes.append(p)

    elif service_type == "filter":
        i = len(running_text_nodes)
        if i >= MAX_NODES:
            return
        port = TEXT_PORT_BASE + i
        name = f"InsultFilterService_{i}"
        cmd = f"python3 InsultFilterService/server.py {port} {name}"
        print(f"[UP] Lanzando {name}")
        p = subprocess.Popen(cmd, shell=True)
        running_text_nodes.append(p)

def scale_down(service_type):
    if service_type == "insult" and len(running_insult_nodes) > MIN_NODES:
        p = running_insult_nodes.pop()
        p.terminate()
        print("[DOWN] InsultService eliminado")

    elif service_type == "filter" and len(running_text_nodes) > MIN_NODES:
        p = running_text_nodes.pop()
        p.terminate()
        print("[DOWN] InsultFilterService eliminado")

def autoscaler_loop():
    # arranca con un nodo de cada tipo
    scale_up("insult")
    scale_up("filter")

    while True:
        insult_backlog = get_queue_backlog(INSULT_QUEUE)
        text_backlog = get_queue_backlog(TEXT_QUEUE)

        print(f"[INFO] insult_queue: {insult_backlog}, text_queue: {text_backlog}")

        if insult_backlog > SCALE_UP_THRESHOLD:
            scale_up("insult")
        elif insult_backlog < SCALE_DOWN_THRESHOLD:
            scale_down("insult")

        if text_backlog > SCALE_UP_THRESHOLD:
            scale_up("filter")
        elif text_backlog < SCALE_DOWN_THRESHOLD:
            scale_down("filter")

        time.sleep(SCALE_INTERVAL)

if __name__ == "__main__":
    autoscaler_loop()
