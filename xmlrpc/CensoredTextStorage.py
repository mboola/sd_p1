# Second node to deploy.

# 
import xmlrpc.client
import sys
import time
from xmlrpc.server import SimpleXMLRPCServer
from xmlrpc.server import SimpleXMLRPCRequestHandler

petitions = int(sys.argv[1])
petitions_processed = 0

# Restrict to a particular path
class RequestHandler(SimpleXMLRPCRequestHandler):
	rpc_paths = ('/RPC2',)

censored_texts = []
shutdown_requested = False

# Create server
with SimpleXMLRPCServer(('localhost', 8004),
						requestHandler = RequestHandler) as censored_text_storage:

	def add_censored_text(text):
		global petitions_processed, shutdown_requested
		censored_texts.append(text)
		petitions_processed = petitions_processed + 1
		if (petitions_processed >= petitions):
			print(f"End time: {time.time()}", flush=True)
			shutdown_requested = True
		return "Censored text added correctly!"
	censored_text_storage.register_function(add_censored_text)

	def get_censored_texts():
		return censored_texts
	censored_text_storage.register_function(get_censored_texts)

	# Getting name server in "http://localhost:8000"
	name_server = xmlrpc.client.ServerProxy('http://localhost:8000')
	name_server.add_censored_text_storage_node("http://localhost:8004")

	# Run the server's main loop
	while not shutdown_requested:
		censored_text_storage.handle_request()