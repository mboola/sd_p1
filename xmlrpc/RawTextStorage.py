# Second node to deploy.

# 

import queue
import xmlrpc.client
import threading
import time
from xmlrpc.server import SimpleXMLRPCServer
from xmlrpc.server import SimpleXMLRPCRequestHandler

# Restrict to a particular path
class RequestHandler(SimpleXMLRPCRequestHandler):
	rpc_paths = ('/RPC2',)

text_to_censor = queue.Queue()

petitions = False

def notify_petitions(name_server):
	global petitions
	while True:
		if petitions:
			insult_publisher_uri = name_server.get_insult_publisher_node()
			if insult_publisher_uri:
				insult_publisher = xmlrpc.client.ServerProxy(insult_publisher_uri)
				insult_publisher.notify_filter_services()
				petitions = False
		time.sleep(5)

# Create server
with SimpleXMLRPCServer(('localhost', 8002),
						requestHandler = RequestHandler) as raw_text_storage:

	def add_text_to_filter(text):
		global petitions
		petitions = True
		print(f"Text to filter added: {text}!")
		text_to_censor.put(text)
		return "Text to filter added correctly!"
	raw_text_storage.register_function(add_text_to_filter)

	def get_text_to_filter():
		print(f"Obtaining text to filter!")
		if (text_to_censor.empty()):
			return ""
		return text_to_censor.get()
	raw_text_storage.register_function(get_text_to_filter)

	# Getting name server in "http://localhost:8000"
	name_server = xmlrpc.client.ServerProxy('http://localhost:8000')
	name_server.add_raw_text_storage_node('http://localhost:8002')

	print("Name Server running in http://localhost:8002!")

	thread = threading.Thread(target=notify_petitions, args=(name_server,), daemon=True)
	thread.start()

	# Run the server's main loop
	raw_text_storage.serve_forever()


