# Third node to start.

#
import time
import xmlrpc.client
import random
import threading
from xmlrpc.server import SimpleXMLRPCServer
from xmlrpc.server import SimpleXMLRPCRequestHandler

# Restrict to a particular path
class RequestHandler(SimpleXMLRPCRequestHandler):
	rpc_paths = ('/RPC2',)

subscribers = []

def notify_subscribers(insult_storage):
	while True:
		insults = insult_storage.get_insults()
		if insults:
			random_insult = random.choice(insults)
			for subscriber_uri in subscribers:
				print(f"Notifying insult '{random_insult}' to subscriber URI '{subscriber_uri}'!")
				subscriber = xmlrpc.client.ServerProxy(subscriber_uri)
				subscriber.notify(random_insult)
		time.sleep(5)

# Create observer server
with SimpleXMLRPCServer(('localhost', 8005),
						requestHandler = RequestHandler) as publisher:

	def register_subscriber(subscriber):
		if subscriber not in subscribers:
			print(f"Registered subscriber URI '{subscriber}'!")
			subscribers.append(subscriber)
		return "Subscriber added correctly!"
	publisher.register_function(register_subscriber)

	# Getting server in "http://localhost:8000"
	name_server = xmlrpc.client.ServerProxy("http://localhost:8000")
	name_server.add_event_publisher_node("http://localhost:8005")

	insult_storage_uri = name_server.get_insult_storage_node()
	insult_storage = xmlrpc.client.ServerProxy(insult_storage_uri)

	print("Publisher running at http://localhost:8005!")

	thread = threading.Thread(target=notify_subscribers, args=(insult_storage,), daemon=True)
	thread.start()

	publisher.serve_forever()
