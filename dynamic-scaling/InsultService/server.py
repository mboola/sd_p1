import Pyro4
import redis
import sys
import logging
import json
import pika
from multiprocessing import Process
import traceback

logging.basicConfig(
	level=logging.INFO,
	format="%(asctime)s [%(levelname)s] %(message)s",
	handlers=[
		logging.FileHandler("insult_service.log", mode="a"),
		logging.StreamHandler()
	]
)

@Pyro4.behavior(instance_mode="single")
class InsultService:
	def __init__(self):
		self.r = redis.Redis(host='localhost', port=6379, decode_responses=True)

	@Pyro4.expose
	def add_insult(self, insult_or_list):
		if isinstance(insult_or_list, str):
			insult_or_list = [insult_or_list]

		results = []
		for insult in insult_or_list:
			insult = insult.lower()
			if not self.r.sismember("insults", insult):
				self.r.sadd("insults", insult)
				#logging.info(f"Insult added: {insult}")
				results.append(f"Insult registered: {insult}")
			else:
				#logging.info(f"Insult already exists: {insult}")
				results.append(f"Insult already registered: {insult}")
		return results

	@Pyro4.expose
	def get_insults(self):
		return list(self.r.smembers("insults"))

	def start_rabbitmq_consumer(self):
		def run():
			print("[Consumer] Process started")
			try:
				#credentials = pika.PlainCredentials("ar", "sar")
				parameters = pika.ConnectionParameters("localhost")
				print("Connecting to RabbitMQ...")
				connection = pika.BlockingConnection(parameters)
				print("Connection established.")

				channel = connection.channel()
				channel.queue_declare(queue="insult_queue", durable=True)
				print("Queue declared: insult_queue")

				def callback(ch, method, properties, body):
					#print(f"Message received: {body}")
					try:
						data = json.loads(body)
						insult = data.get("insult")
						if insult:
							self.add_insult(insult)
							ch.basic_ack(delivery_tag=method.delivery_tag)
							#print(f"Insult processed: {insult}")
					except Exception:
						print("Error in callback:")
						traceback.print_exc()

				channel.basic_qos(prefetch_count=1)
				channel.basic_consume(queue="insult_queue", on_message_callback=callback)
				print("[READY] Waiting for messages...")
				channel.start_consuming()

			except Exception:
				print("[Fatal] Error in RabbitMQ consumer process:")
				traceback.print_exc()

		Process(target=run, daemon=True).start()

port = int(sys.argv[1])  # >= 49152
name = sys.argv[2]       # e.g. InsultService_0

print(port)

obj = InsultService()
obj.start_rabbitmq_consumer()

daemon = Pyro4.Daemon(port=port)
ns = Pyro4.locateNS()
uri = daemon.register(obj)
ns.register(name, uri)
logging.info(f"{name} registered at {uri}")
daemon.requestLoop()
