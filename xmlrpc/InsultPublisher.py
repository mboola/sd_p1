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

my_insults = []
insult_filters = []
update = False
notify = False

def update_insult_filters():
	global update
	global notify
	while True:
		if update or notify:
			for insult_filter_worker_uri in insult_filters:
				insult_filter_worker = xmlrpc.client.ServerProxy(insult_filter_worker_uri)
				if update:
					insult_filter_worker.update_insult_list(my_insults)
				else:
					insult_filter_worker.awake()
			update = False
			notify = False
		time.sleep(5)

# Create observer server
with SimpleXMLRPCServer(('localhost', 8006),
						requestHandler = RequestHandler) as insult_publisher:

	def update_insults(insults):
		my_insults.append(insults)
		update = True
		return "New insults appended correctly!"
	insult_publisher.register_function(update_insults)

	def notify_filter_services():
		notify = True
		return ""
	insult_publisher.register_function(notify_filter_services)

	# Getting server in "http://localhost:8000"
	name_server = xmlrpc.client.ServerProxy("http://localhost:8000")
	name_server.add_insult_publisher_node("http://localhost:8006")
	
	insult_filters = name_server.get_insult_filter_workers()
	
	print("Storage Publisher running in http://localhost:8006!")

	thread = threading.Thread(target=update_insult_filters, daemon=True)
	thread.start()

	insult_publisher.serve_forever()
	
