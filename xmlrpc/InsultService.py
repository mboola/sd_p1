# Third node to start.

#

import sys
import time
import threading
import xmlrpc.client
from xmlrpc.server import SimpleXMLRPCServer
from xmlrpc.server import SimpleXMLRPCRequestHandler

# Restrict to a particular path
class RequestHandler(SimpleXMLRPCRequestHandler):
	rpc_paths = ('/RPC2',)

# If there is a port inputed as a parameter
if len(sys.argv) > 1:

	last_updated_insults = []
	new_insults = []

	# Separate thread that gets updated insults of insult storage sending its
	# own new insults
	def update_insults(insult_storage):
		global last_updated_insults
		global new_insults
		while True:
			time.sleep(10)
			#print(new_insults)
			insult_storage.update_insults(new_insults)
			for insult in new_insults:
				last_updated_insults.append(insult)
			new_insults = []

	# Create observer server
	with SimpleXMLRPCServer(('localhost', int(sys.argv[1])),
							requestHandler = RequestHandler) as insult_service:

		# Called from clients
		def add_insult(insult):
			if insult not in last_updated_insults:
				if insult not in new_insults:
					new_insults.append(insult)
					#print(f"Added insult '{insult}' to new insults!")
			return "List updated!"
		insult_service.register_function(add_insult)

		# Getting server in "http://localhost:8000"
		name_server = xmlrpc.client.ServerProxy("http://localhost:8000")
		name_server.add_insult_worker("http://localhost:" + sys.argv[1])

		storage_node_uri = name_server.get_insult_storage_node()
		insult_storage = xmlrpc.client.ServerProxy(storage_node_uri)

		print("Insult Service running in http://localhost:" + sys.argv[1] + "!")

		thread = threading.Thread(target=update_insults, args=(insult_storage,), daemon=True)
		thread.start()

		try:
			insult_service.serve_forever()
		except KeyboardInterrupt:
			print("\nShutting down server...")
			insult_service.server_close()
