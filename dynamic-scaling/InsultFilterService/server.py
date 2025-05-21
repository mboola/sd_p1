import redis
import sys
import json
import pika
import re
import signal

port = int(sys.argv[1])  # >= 49152
name = sys.argv[2]       # e.g. InsultService_0

original_stdout = sys.stdout

log_file = open(f"logging/{name}.log", "a")
sys.stdout = log_file
sys.stderr = log_file

result_queue = "filtered_texts"

def cleanup(signum, frame):
	print(f"Insult service not running with name {name}", flush=True)
	sys.stdout = original_stdout
	log_file.close()
	sys.exit(0)

signal.signal(signal.SIGINT, cleanup)  # Optional: handle Ctrl+C too

redis_server = redis.Redis(host='localhost', port=6379, decode_responses=True)


def get_insults_list():
	return redis_server.smembers("insults")

def filter_text(text):
	my_insults = get_insults_list()

	for insult in my_insults:
		text = re.sub(insult, "CENSORED", text, flags=re.IGNORECASE)

	return text

def add_text(input_texts):
	if isinstance(input_texts, str):
		input_texts = [input_texts]

	for text in input_texts:
		text = text.lower()
		filtered = filter_text(text)
		redis_server.rpush(result_queue, filtered)

def get_texts():
	return redis_server.lrange(result_queue, 0, -1)

print(f"Insult Filter service running at port {port} with name {name}", flush=True)

#credentials = pika.PlainCredentials("ar", "sar")
parameters = pika.ConnectionParameters("localhost")
print("Connecting to RabbitMQ...")
connection = pika.BlockingConnection(parameters)
print("Connection established.")

channel = connection.channel()
channel.queue_declare(queue="text_queue", durable=True)
print("Queue declared: text_queue")

def callback(ch, method, properties, body):
	data = json.loads(body)
	text = data.get("text")
	if text:
		add_text(text)
		ch.basic_ack(delivery_tag=method.delivery_tag)

channel.basic_qos(prefetch_count=1)
channel.basic_consume(queue="text_queue", on_message_callback=callback)
print("[READY] Waiting for messages on text_queue...")
channel.start_consuming()
