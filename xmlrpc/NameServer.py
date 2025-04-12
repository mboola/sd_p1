# First node to deploy.

# Name server that will store the URIs of all the nodes of both services,
# the publisher, the insult storage and both raw and censored text storage.

from xmlrpc.server import SimpleXMLRPCServer
from xmlrpc.server import SimpleXMLRPCRequestHandler

# Restrict to a particular path
class RequestHandler(SimpleXMLRPCRequestHandler):
	rpc_paths = ('/RPC2',)

# Create server
with SimpleXMLRPCServer(('localhost', 8000),
						requestHandler = RequestHandler) as name_server:

	insult_service_workers = []
	insult_filter_service_workers = []
	insult_storage_node = ""
	insult_publisher_node = ""
	raw_text_storage_node = ''
	censored_text_storage_node = ''
	publisher_node = ""

	def add_insult_worker(worker):
		# TODO : check if worker is inside insult_service_workers.
		# if it is not, add it
		insult_service_workers.append(worker)
		return "Node added correctly!"
	name_server.register_function(add_insult_worker)

	def get_insult_workers():
		return insult_service_workers
	name_server.register_function(get_insult_workers)

	def add_insult_filter_worker(worker):
		# TODO : check if worker is inside insult_service_workers.
		# if it is not, add it
		insult_filter_service_workers.append(worker)
		return "Node added correctly!"
	name_server.register_function(add_insult_filter_worker)

	def get_insult_filter_workers():
		return insult_filter_service_workers
	name_server.register_function(get_insult_filter_workers)

	def add_publisher_node(publisher):
		publisher_node = publisher
		return "Publisher added correctly!"
	name_server.register_function(add_publisher_node)

	def get_publisher_node():
		return publisher_node
	name_server.register_function(get_publisher_node)

	def add_insult_storage_node(insult_storage):
		insult_storage_node = insult_storage
		return "Insult storage added correctly!"
	name_server.register_function(add_insult_storage_node)

	def get_insult_storage_node():
		return insult_storage_node
	name_server.register_function(get_insult_storage_node)

	def add_insult_publisher_node(insult_publisher):
		insult_publisher_node = insult_publisher
		return "Insult storage added correctly!"
	name_server.register_function(add_insult_publisher_node)

	def get_insult_publisher_node():
		return insult_publisher_node
	name_server.register_function(get_insult_publisher_node)
	
	def add_raw_text_storage_node(raw_text_storage):
		raw_text_storage_node = raw_text_storage
		print(raw_text_storage_node)
		return "Raw text storage added correctly!"
	name_server.register_function(add_raw_text_storage_node)

	def get_raw_text_storage_node():
		print(raw_text_storage_node)
		return raw_text_storage_node
	name_server.register_function(get_raw_text_storage_node)

	def add_censored_text_storage_node(censored_text_storage):
		censored_text_storage_node = censored_text_storage
		return "Censored text storage added correctly!"
	name_server.register_function(add_censored_text_storage_node)

	def get_censored_text_storage_node():
		return censored_text_storage_node
	name_server.register_function(get_censored_text_storage_node)

	print("Name server started!")

	# Run the server's main loop
	name_server.serve_forever()
