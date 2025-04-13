# Second node to deploy.

# 

import queue
import xmlrpc.client

from xmlrpc.server import SimpleXMLRPCServer
from xmlrpc.server import SimpleXMLRPCRequestHandler

# Restrict to a particular path
class RequestHandler(SimpleXMLRPCRequestHandler):
	rpc_paths = ('/RPC2',)

text_to_censor = queue.Queue()

petitions = False

# Create server
with SimpleXMLRPCServer(('localhost', 8002),
						requestHandler = RequestHandler) as raw_text_storage:

	def add_text_to_filter(text):
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

	insult_publisher = name_server.get_insult_publisher_node()

	print("Name Server running in http://localhost:8002!")

	# Run the server's main loop
	raw_text_storage.serve_forever()

	while True:
		time.sleep(5)
		if petitions:
			insult_publisher.notify_filter_services()
			petitions = False

