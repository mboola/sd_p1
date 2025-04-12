# Third node to start.

#

import sys
import time

from xmlrpc.server import SimpleXMLRPCServer
from xmlrpc.server import SimpleXMLRPCRequestHandler

# Restrict to a particular path
class RequestHandler(SimpleXMLRPCRequestHandler):
	rpc_paths = ('/RPC2',)


# If there is a port inputed as a parameter
if len(sys.argv) > 1:

	last_updated_insults = []
	new_insults = []

	storage_node_uri = ""

	# Create observer server
	with SimpleXMLRPCServer(('localhost', int(sys.argv[1])),
							requestHandler = RequestHandler) as insult_service:

		def add_insult(insult):
			if insult not in last_updated_insults:
				if insult not in new_insults:
					new_insults.append(insult)
			return "List updated!"
		insult_service.register_function(add_insult)

		def get_insults():
			new_list = last_updated_insults
			new_list.append(new_insults)
			return new_list
		insult_service.register_function(get_insults)

		# Getting server in "http://localhost:8000"
		name_server = xmlrpc.client.ServerProxy("http://localhost:8000")
		name_server.add_insult_service_worker("http://localhost:" + sys.argv[1])

		storage_node_uri = name_server.get_insult_storage_node()
		insult_storage = xmlrpc.client.ServerProxy(storage_node_uri)

		while True:
			updated_insults = insult_storage.update_insults(new_insults)
			last_updated_insults.append(new_insults)
			new_insults = []
			for insult in updated_insults:
				if insult not in last_updated_insults:
					last_updated_insults.append(insult)
			time.sleep(3)
