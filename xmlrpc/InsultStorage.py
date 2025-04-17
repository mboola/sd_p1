# Third node to start.

#
import time
import xmlrpc.client
import threading
from xmlrpc.server import SimpleXMLRPCServer
from xmlrpc.server import SimpleXMLRPCRequestHandler

# Restrict to a particular path
class RequestHandler(SimpleXMLRPCRequestHandler):
	rpc_paths = ('/RPC2',)

last_updated_insults = []
new_insults = []

def notify_insults(insult_publisher):
	global new_insults
	while True:
		if new_insults:
			insult_publisher.update_insults(new_insults)
			for insult in new_insults:
				if insult not in last_updated_insults:
					last_updated_insults.append(insult)
					print(f"Added '{insult}' insult_publisher!")
			new_insults = []
		time.sleep(5)

# Create observer server
with SimpleXMLRPCServer(('localhost', 8003),
						requestHandler = RequestHandler) as insult_storage:

	def update_insults(insults):
		global last_updated_insults
		global new_insults
		print(f"Insults: '{insults}'!")
		if insults:
			for insult in insults:
				if insult not in last_updated_insults:
					if insult not in new_insults:
						new_insults.append(insult)
						print(f"Added insult '{insult}' to new insults!")
			new_list = last_updated_insults
			for insult in new_insults:
				new_list.append(insult)
			return new_list
		return last_updated_insults
	insult_storage.register_function(update_insults)

	def get_insults():
		global last_updated_insults
		new_list = last_updated_insults
		for insult in new_insults:
			new_list.append(insult)
		return new_list
	insult_storage.register_function(get_insults)

	# Getting server in "http://localhost:8000"
	name_server = xmlrpc.client.ServerProxy("http://localhost:8000")
	name_server.add_insult_storage_node("http://localhost:8003")

	insult_publisher_uri = name_server.get_insult_publisher_node()
	insult_publisher = xmlrpc.client.ServerProxy(insult_publisher_uri)
	
	print("Insult Storage running in http://localhost:8003!")

	thread = threading.Thread(target=notify_insults, args=(insult_publisher,), daemon=True)
	thread.start()

	insult_storage.serve_forever()
