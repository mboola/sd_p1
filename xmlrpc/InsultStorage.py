# Third node to start.

#
import time

from xmlrpc.server import SimpleXMLRPCServer
from xmlrpc.server import SimpleXMLRPCRequestHandler

# Restrict to a particular path
class RequestHandler(SimpleXMLRPCRequestHandler):
	rpc_paths = ('/RPC2',)

last_updated_insults = []
new_insults = []

publisher_storage_uri = ""

# Create observer server
with SimpleXMLRPCServer(('localhost', 8003),
						requestHandler = RequestHandler) as insult_storage:

	def update_insults(insults):
		for insult in insults:
			if insult not in last_updated_insults:
				if insult not in new_insults:
					new_insults.append(insult)
		new_list = last_updated_insults
		new_list.append(new_insults)
		return new_list
	insult_storage.register_function(update_insults)

	def get_insults():
		new_list = last_updated_insults
		new_list.append(new_insults)
		return new_list
	insult_storage.register_function(get_insults)

	# Getting server in "http://localhost:8000"
	name_server = xmlrpc.client.ServerProxy("http://localhost:8000")
	name_server.add_insult_storage_node("http://localhost:8003")

	publisher_storage_uri = name_server.get_insult_publisher_node()
	publisher_storage = xmlrpc.client.ServerProxy(publisher_storage_uri)

	while True:
		if ! new_insults.isEmpty():
			publisher_storage.update_insults(new_insults)
			last_updated_insults.append(new_insults)
			new_insults = []
		time.sleep(5)
