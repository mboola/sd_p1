# First node to deploy
import time
import random
from xmlrpc.server import SimpleXMLRPCServer
from xmlrpc.server import SimpleXMLRPCRequestHandler

# Restrict to a particular path
class RequestHandler(SimpleXMLRPCRequestHandler):
	rpc_paths = ('/RPC2',)

insults = []
filtered_texts = []
subscribers = []

# Create server
with SimpleXMLRPCServer(('localhost', 8001),
						requestHandler = RequestHandler) as broadcaster_server:

	def update_insults(new_insults):
		for new_insult in new_insults:
			# TODO : check if insults are inside insults.
			# if they are not, add them
			insults.appdend(new_insult)
		return insults # full list of insults
	name_server.register_function(update_insults)

	def register_subscriber(subscriber):
		# TODO : check if subscriber is not already inside subscribers
		# if they are not, add them
		subscribers.appdend(subscriber)
		return "Subscriber '" + subscriber + "' added."
	name_server.register_function(register_subscriber)

	def add_filtered_text(filtered_text):
		filtered_texts.append(filtered_text)
		return "Text added"
	name_server.register_function(add_filtered_text)

	while True:
		# TODO : check if filtered texts is not empty then do:
		random_text = random.choice(filtered_texts)
		for subscriber in subscribers:
			xmlrpc.client.ServerProxy(subscriber).notify(random_text)
		time.sleep(5)
