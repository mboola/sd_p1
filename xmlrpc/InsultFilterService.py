# Third node to start.

#

import sys
import time
import xmlrpc.client
from xmlrpc.server import SimpleXMLRPCServer
from xmlrpc.server import SimpleXMLRPCRequestHandler

# Restrict to a particular path
class RequestHandler(SimpleXMLRPCRequestHandler):
	rpc_paths = ('/RPC2',)

# If there is a port inputed as a parameter
if len(sys.argv) > 1:

	my_insults = []

	# Create observer server
	with SimpleXMLRPCServer(('localhost', int(sys.argv[1])),
							requestHandler = RequestHandler) as insult_filter:

		def update_insult_list(insults):
			my_insults = insults
			return "List updated!"
		insult_filter.register_function(update_insult_list)

		# Getting server in "http://localhost:8000"
		name_server = xmlrpc.client.ServerProxy("http://localhost:8000")
		name_server.add_insult_filter_worker("http://localhost:" + sys.argv[1])
		
		raw_text_storage_uri = name_server.get_raw_text_storage_node()
		print(f"Raw Text URI:, {raw_text_storage_uri}!")
		raw_text_storage_server = xmlrpc.client.ServerProxy(raw_text_storage_uri)

		censored_text_storage_uri = name_server.get_censored_text_storage_node()
		censored_text_storage_server = xmlrpc.client.ServerProxy(censored_text_storage_uri)

		print("Insult Filter Service started!")

		while True:
			text = raw_text_storage_server.get_text_to_filter()
			if text != "":
				for insult in my_insults:
					text = re.sub(insult, "CENSORED", text, flags=re.IGNORECASE)
				censored_text_storage_server.add_censored_text(text)
			time.sleep(1)
