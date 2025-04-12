# Third node to start.

#
import time

from xmlrpc.server import SimpleXMLRPCServer
from xmlrpc.server import SimpleXMLRPCRequestHandler

# Restrict to a particular path
class RequestHandler(SimpleXMLRPCRequestHandler):
	rpc_paths = ('/RPC2',)

my_insults = []
insult_filters = []
update = False

# Create observer server
with SimpleXMLRPCServer(('localhost', 8006),
						requestHandler = RequestHandler) as storage_publisher:

	def update_insults(insults):
		my_insults.append(insults)
		update = True
		return "New insults appended correctly!"
	storage_publisher.register_function(update_insults)


	# Getting server in "http://localhost:8000"
	name_server = xmlrpc.client.ServerProxy("http://localhost:8000")
	name_server.add_insult_publisher_node("http://localhost:8006")

	publisher_storage_uri = name_server.get_insult_publisher_node()
	publisher_storage = xmlrpc.client.ServerProxy(publisher_storage_uri)

	insult_filters = name_server.get_insult_filter_workers()

	while True:
		if update:
			for insult_filter_worker_uri in insult_filters:
				insult_filter_worker = xmlrpc.client.ServerProxy(insult_filter_worker_uri)
				insult_filter_worker.update_insult_list(my_insults)
			update = False
		time.sleep(5)
