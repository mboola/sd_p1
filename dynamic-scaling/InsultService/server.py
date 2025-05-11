import Pyro4
import redis
import sys
import json
import pika
import traceback
import signal
import threading

port = int(sys.argv[1])  # >= 49152
name = sys.argv[2]       # e.g. InsultService_0

original_stdout = sys.stdout

log_file = open(f"logging/{name}.log", "a")
sys.stdout = log_file
sys.stderr = log_file

def cleanup(signum, frame):
	print(f"Insult service not running with name {name}", flush=True)
	ns = Pyro4.locateNS()
	ns.remove(name)
	sys.stdout = original_stdout
	log_file.close()
	sys.exit(0)

signal.signal(signal.SIGINT, cleanup)  # Optional: handle Ctrl+C too

@Pyro4.behavior(instance_mode="single")
class InsultService:
	def __init__(self):
		self.r = redis.Redis(host='localhost', port=6379, decode_responses=True)

	@Pyro4.expose
	def add_insult(self, insult_or_list):
		if isinstance(insult_or_list, str):
			insult_or_list = [insult_or_list]

		for insult in insult_or_list:
			insult = insult.lower()
			if not self.r.sismember("insults", insult):
				self.r.sadd("insults", insult)

	@Pyro4.expose
	def get_insults(self):
		return list(self.r.smembers("insults"))

	def start_rabbitmq_consumer(self):
		print("[Consumer] Process started", flush=True)
		try:
			#credentials = pika.PlainCredentials("ar", "sar")
			parameters = pika.ConnectionParameters("localhost")
			print("Connecting to RabbitMQ...", flush=True)
			connection = pika.BlockingConnection(parameters)
			print("Connection established.", flush=True)

			channel = connection.channel()
			channel.queue_declare(queue="insult_queue", durable=True)
			print("Queue declared: insult_queue", flush=True)

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
			print("[READY] Waiting for messages...", flush=True)
			channel.start_consuming()

		except Exception:
			print("[Fatal] Error in RabbitMQ consumer process:")
			traceback.print_exc()

print(f"Insult service running at port {port} with name {name}", flush=True)

obj = InsultService()

# Start Pyro4 server
daemon = Pyro4.Daemon(port=port)
ns = Pyro4.locateNS()
uri = daemon.register(obj)
ns.register(name, uri)

# Start the RabbitMQ consumer in a separate thread
threading.Thread(target=obj.start_rabbitmq_consumer, daemon=True).start()

daemon.requestLoop()
