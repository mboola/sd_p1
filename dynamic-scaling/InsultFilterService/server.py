import Pyro4
import redis
import sys
import json
import pika
import re
from datetime import datetime, timezone
import traceback
import signal
import threading

port = int(sys.argv[1])  # >= 49152
name = sys.argv[2]       # e.g. InsultService_0

original_stdout = sys.stdout

log_file = open(f"logging/{name}.log", "a")
sys.stdout = log_file
sys.stderr = log_file

result_queue = "filtered_texts"

def cleanup(signum, frame):
	print(f"Insult service not running with name {name}", flush=True)
	ns = Pyro4.locateNS()
	ns.remove(name)
	sys.stdout = original_stdout
	log_file.close()
	sys.exit(0)

signal.signal(signal.SIGINT, cleanup)  # Optional: handle Ctrl+C too

@Pyro4.behavior(instance_mode="single")
class InsultFilterService:
	def __init__(self):
		self.r = redis.Redis(host='localhost', port=6379, decode_responses=True)

	def get_insults_list(self):
		return self.r.smembers("insults")

	def filter_text(self, text):
		my_insults = self.get_insults_list()

		for insult in my_insults:
			text = re.sub(insult, "CENSORED", text, flags=re.IGNORECASE)

		return text

	@Pyro4.expose
	def add_text(self, input_texts):
		if isinstance(input_texts, str):
			input_texts = [input_texts]

		for text in input_texts:
			text = text.lower()
			filtered = self.filter_text(text)
			self.r.rpush(result_queue, filtered)

	@Pyro4.expose
	def get_texts(self):
		return self.r.lrange(result_queue, 0, -1)

	def start_rabbitmq_consumer(self):
		print("[Consumer] Process started for text_queue")
		try:
			#credentials = pika.PlainCredentials("ar", "sar")
			parameters = pika.ConnectionParameters("localhost")
			print("Connecting to RabbitMQ...")
			connection = pika.BlockingConnection(parameters)
			print("Connection established.")

			channel = connection.channel()
			channel.queue_declare(queue="text_queue", durable=True)
			print("Queue declared: text_queue")

			def callback(ch, method, properties, body):
				#print(f"Message received: {body}")
				try:
					data = json.loads(body)
					text = data.get("text")
					if text:
						self.add_text(text)
						ch.basic_ack(delivery_tag=method.delivery_tag)
						#print(f"Text processed: {text}")
				except Exception:
					print("Error in callback:")
					traceback.print_exc()

			channel.basic_qos(prefetch_count=1)
			channel.basic_consume(queue="text_queue", on_message_callback=callback)
			print("[READY] Waiting for messages on text_queue...")
			channel.start_consuming()

		except Exception:
			print("[Fatal] Error in RabbitMQ consumer process:")
			traceback.print_exc()

print(f"Insult Filter service running at port {port} with name {name}", flush=True)

obj = InsultFilterService()

# Start Pyro4 server
daemon = Pyro4.Daemon(port=port)
ns = Pyro4.locateNS()
uri = daemon.register(obj)
ns.register(name, uri)

# Start the RabbitMQ consumer in a separate thread
threading.Thread(target=obj.start_rabbitmq_consumer, daemon=True).start()

daemon.requestLoop()
