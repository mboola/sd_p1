# Third node to start.

#
import sys
import xmlrpc.client
from xmlrpc.server import SimpleXMLRPCServer
from socketserver import ThreadingMixIn
from time import sleep
import threading

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
			sleep(10)
			#print(new_insults)
			insult_storage.update_insults(new_insults)
			for insult in new_insults:
				last_updated_insults.append(insult)
			new_insults = []
		
	# Called from clients
	def add_insult(insult):
		if insult not in last_updated_insults:
			if insult not in new_insults:
				new_insults.append(insult)
				#print(f"Added insult '{insult}' to new insults!")
		return "List updated!"
	
	class ThreadedXMLRPCServer(ThreadingMixIn, SimpleXMLRPCServer):
		pass

	insult_service = ThreadedXMLRPCServer(('localhost', int(sys.argv[1])))
	insult_service.socket.settimeout(10) #timeout 10 seconds

	insult_service.register_function(add_insult)

	# Getting server in "http://localhost:8000"
	name_server = xmlrpc.client.ServerProxy("http://localhost:8000")
	name_server.add_insult_worker("http://localhost:" + sys.argv[1])

	storage_node_uri = name_server.get_insult_storage_node()
	insult_storage = xmlrpc.client.ServerProxy(storage_node_uri)

	print("Insult Service running in http://localhost:" + sys.argv[1] + "!")

	thread = threading.Thread(target=update_insults, args=(insult_storage,), daemon=True)
	thread.start()

	insult_service.serve_forever()
