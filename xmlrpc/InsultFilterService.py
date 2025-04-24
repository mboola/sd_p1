# Third node to start.

#
import re
import sys
import xmlrpc.client
import threading
from xmlrpc.server import SimpleXMLRPCServer
from xmlrpc.server import SimpleXMLRPCRequestHandler

# Restrict to a particular path
class RequestHandler(SimpleXMLRPCRequestHandler):
	rpc_paths = ('/RPC2',)

# If there is a port inputed as a parameter
if len(sys.argv) > 1:

	my_insults = []
	awake = False

	def filter_texts(raw_text_storage_server, censored_text_storage_server):
		global awake
		while True:
			if awake:
				text = raw_text_storage_server.get_text_to_filter()
				print(text)
				if text:
					for insult in my_insults:
						text = re.sub(insult, "CENSORED", text, flags=re.IGNORECASE)
					print(text)
					censored_text_storage_server.add_censored_text(text)
				else:
					awake = False

	# Create observer server
	with SimpleXMLRPCServer(('localhost', int(sys.argv[1])),
							requestHandler = RequestHandler) as insult_filter:

		# Called from insult 
		def update_insult_list(insults):
			global my_insults
			my_insults = []
			for insult in insults:
				my_insults.append(insult)
			print(f"New list of insults '{my_insults}'")
			return "List updated!"
		insult_filter.register_function(update_insult_list)

		def awake():
			global awake
			print("Notified!")
			awake = True
			return ""
		insult_filter.register_function(awake)

		# Getting server in "http://localhost:8000"
		name_server = xmlrpc.client.ServerProxy("http://localhost:8000")
		name_server.add_insult_filter_worker("http://localhost:" + sys.argv[1])
		
		raw_text_storage_uri = name_server.get_raw_text_storage_node()
		print(f"Raw Text URI: {raw_text_storage_uri}!")
		raw_text_storage_server = xmlrpc.client.ServerProxy(raw_text_storage_uri)

		censored_text_storage_uri = name_server.get_censored_text_storage_node()
		print(f"Raw Text URI: {censored_text_storage_uri}!")
		censored_text_storage_server = xmlrpc.client.ServerProxy(censored_text_storage_uri)

		print("Insult Filter Service running in http://localhost:" + sys.argv[1] + "!")

		thread = threading.Thread(target=filter_texts, args=(raw_text_storage_server, censored_text_storage_server,), daemon=True)
		thread.start()

		insult_filter.serve_forever()