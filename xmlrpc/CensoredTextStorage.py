# Second node to deploy.

# 

import xmlrpc.client
from xmlrpc.server import SimpleXMLRPCServer
from xmlrpc.server import SimpleXMLRPCRequestHandler

# Restrict to a particular path
class RequestHandler(SimpleXMLRPCRequestHandler):
	rpc_paths = ('/RPC2',)

censored_texts = ["papanatas"]

# Create server
with SimpleXMLRPCServer(('localhost', 8004),
						requestHandler = RequestHandler) as censored_text_storage:

	def add_censored_text(text):
		censored_texts.append(text)
		#print(f"Added '{text}' to Censored Text Storage!")
		return "Censored text added correctly!"
	censored_text_storage.register_function(add_censored_text)

	def get_censored_texts():
		return censored_texts
	censored_text_storage.register_function(get_censored_texts)

	# Getting name server in "http://localhost:8000"
	name_server = xmlrpc.client.ServerProxy('http://localhost:8000')
	name_server.add_censored_text_storage_node("http://localhost:8004")

	print("Censored Text Storage started!")

	# Run the server's main loop
	censored_text_storage.serve_forever()
