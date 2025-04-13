# First node to deploy.

# Name server that will store the URIs of all the nodes of both services,
# the publisher, the insult storage and both raw and censored text storage.

from xmlrpc.server import SimpleXMLRPCServer
from xmlrpc.server import SimpleXMLRPCRequestHandler

# Restrict to a particular path
class RequestHandler(SimpleXMLRPCRequestHandler):
	rpc_paths = ('/RPC2',)

raw_text_storage_node = ''
censored_text_storage_node = ''
insult_service_workers = []
insult_filter_service_workers = []
insult_storage_node = ""
insult_publisher_node = ""
event_publisher_node = ""

# Create server
with SimpleXMLRPCServer(('localhost', 8000),
						requestHandler = RequestHandler) as name_server:

	def add_insult_worker(worker):
		if worker not in insult_service_workers:
			insult_service_workers.append(worker)
			print(f"Added URI: '{worker}' to insult_service_workers!")
			return "Node added correctly!"
		return "Node already added!"
	name_server.register_function(add_insult_worker)

	def get_insult_workers():
		return insult_service_workers
	name_server.register_function(get_insult_workers)

	def add_insult_filter_worker(worker):
		if worker not in insult_filter_service_workers:
			insult_filter_service_workers.append(worker)
			print(f"Added URI: '{worker}' to insult_filter_service_workers!")
			return "Node added correctly!"
		return "Node already added!"
	name_server.register_function(add_insult_filter_worker)

	def get_insult_filter_workers():
		return insult_filter_service_workers
	name_server.register_function(get_insult_filter_workers)

	def add_event_publisher_node(event_publisher):
		global event_publisher_node
		event_publisher_node = event_publisher
		print(f"Added URI: '{event_publisher_node}' as Publisher!")
		return "Publisher added correctly!"
	name_server.register_function(add_event_publisher_node)

	def get_event_publisher_node():
		return event_publisher_node
	name_server.register_function(get_event_publisher_node)

	def add_insult_storage_node(insult_storage):
		global insult_storage_node
		insult_storage_node = insult_storage
		print(f"Added URI: '{insult_storage_node}' as Insult Storage!")
		return "Insult storage added correctly!"
	name_server.register_function(add_insult_storage_node)

	def get_insult_storage_node():
		return insult_storage_node
	name_server.register_function(get_insult_storage_node)

	def add_insult_publisher_node(insult_publisher):
		global insult_publisher_node
		insult_publisher_node = insult_publisher
		print(f"Added URI: '{insult_publisher_node}' as Storage Publisher!")
		return "Insult storage added correctly!"
	name_server.register_function(add_insult_publisher_node)

	def get_insult_publisher_node():
		return insult_publisher_node
	name_server.register_function(get_insult_publisher_node)
	
	def add_raw_text_storage_node(raw_text_storage):
		global raw_text_storage_node
		raw_text_storage_node = raw_text_storage
		return "Raw text storage added correctly!"
	name_server.register_function(add_raw_text_storage_node)

	def get_raw_text_storage_node():
		return raw_text_storage_node
	name_server.register_function(get_raw_text_storage_node)

	def add_censored_text_storage_node(censored_text_storage):
		global censored_text_storage_node
		censored_text_storage_node = censored_text_storage
		return "Censored text storage added correctly!"
	name_server.register_function(add_censored_text_storage_node)

	def get_censored_text_storage_node():
		return censored_text_storage_node
	name_server.register_function(get_censored_text_storage_node)

	print("Name Server running in http://localhost:8000!")

	# Run the server's main loop
	name_server.serve_forever()
