# Third node to start.

#

import sys
import time

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
							requestHandler = RequestHandler) as subscriber:

		def notify(insult):
			print(insult)
			return "Insult printed!"
		subscriber.register_function(notify)

		# Getting server in "http://localhost:8000"
		name_server = xmlrpc.client.ServerProxy("http://localhost:8000")

        publisher_uri = name_server.get_publisher_node()
        publisher = xmlrpc.client.ServerProxy(publisher_uri)
        publisher.register_subscriber("http://localhost:" + sys.argv[1])

		# Run the server's main loop
	    subscriber.serve_forever()

