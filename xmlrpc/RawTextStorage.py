# Second node to deploy.

# 

import queue

from xmlrpc.server import SimpleXMLRPCServer
from xmlrpc.server import SimpleXMLRPCRequestHandler

# Restrict to a particular path
class RequestHandler(SimpleXMLRPCRequestHandler):
	rpc_paths = ('/RPC2',)

text_to_censor = queue.Queue()

# Create server
with SimpleXMLRPCServer(('localhost', 8002),
						requestHandler = RequestHandler) as raw_text_storage:

	def add_text_to_filter(text):
		text_to_censor.put(text)
		return "Text to filter added correctly!"
	server.register_function(add_text_to_filter)

	def get_text_to_filter():
		if (text_to_censor.empty()):
			return ""
		return text_to_censor.get()
	server.register_function(get_text_to_filter)

	# Getting name server in "http://localhost:8000"
	name_server = xmlrpc.client.ServerProxy('http://localhost:8000')
	name_server.add_raw_text_storage_node("http://localhost:8002")

	# Run the server's main loop
	server.serve_forever()
