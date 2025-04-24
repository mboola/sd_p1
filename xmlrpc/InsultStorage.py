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

insult_storage_list = []
recently_added_insults = []

# 
def notify_insults(insult_publisher):
	global recently_added_insults
	while True:
		if recently_added_insults:
			insult_publisher.update_insults(recently_added_insults)
			for insult in recently_added_insults:
				if insult not in insult_storage_list:
					insult_storage_list.append(insult)
					print(f"Added '{insult}' insult_publisher!")
			recently_added_insults = []
		time.sleep(5)

# Create observer server
with SimpleXMLRPCServer(('localhost', 8003),
						requestHandler = RequestHandler) as insult_storage:

	# Called from InsultService nodes. Adds insults to storage and return
	# all insults currently storage.
	def update_insults(new_insults):
		global insult_storage_list
		global recently_added_insults
		print(f"Trying to add insults: '{new_insults}'!")
		if not new_insults:
			return insult_storage_list
		for insult in new_insults:
			if insult not in insult_storage_list:
				if insult not in recently_added_insults:
					recently_added_insults.append(insult)
					print(f"Added insult '{insult}' to recently added insults!")
		new_list = []
		for insult in insult_storage_list:
			new_list.append(insult)
		for insult in recently_added_insults:
			new_list.append(insult)
		return new_list
	insult_storage.register_function(update_insults)

	def get_insults():
		new_list = []
		for insult in insult_storage_list:
			new_list.append(insult)
		for insult in recently_added_insults:
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
