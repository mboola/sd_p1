# Third node to start.

#
import time

from xmlrpc.server import SimpleXMLRPCServer
from xmlrpc.server import SimpleXMLRPCRequestHandler

# Restrict to a particular path
class RequestHandler(SimpleXMLRPCRequestHandler):
	rpc_paths = ('/RPC2',)

subscribers = []

# Create observer server
with SimpleXMLRPCServer(('localhost', 8005),
						requestHandler = RequestHandler) as publisher:

	def register_subscriber(subscriber):
		if subscriber not in subscribers:
            subscribers.append(subscriber)
		return "Subscriber added correctly!"
	publisher.register_function(register_subscriber)

	# Getting server in "http://localhost:8000"
	name_server = xmlrpc.client.ServerProxy("http://localhost:8000")
	name_server.add_publisher_node("http://localhost:8005")

	insult_storage_uri = name_server.get_insult_storage_node()
	insult_storage = xmlrpc.client.ServerProxy(insult_storage_uri)

	while True:
        insults = insult_storage.get_insults()
        random_insult = random.choice(insults)
		for subscriber_uri in subscribers:
            subscriber = xmlrpc.client.ServerProxy(subscriber_uri)
            subscriber.notify(random_insult)
		time.sleep(5)
