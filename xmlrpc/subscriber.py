import sys
import xmlrpc.client
from xmlrpc.server import SimpleXMLRPCServer
from xmlrpc.server import SimpleXMLRPCRequestHandler

# Restrict to a particular path
class RequestHandler(SimpleXMLRPCRequestHandler):
	rpc_paths = ('/RPC2',)

if len(sys.argv) > 1:
	# Create observer server
	with SimpleXMLRPCServer(('localhost', int(sys.argv[1])),
							requestHandler = RequestHandler) as subscriber_server:
		subscriber_server.register_introspection_functions()

		def notify(text):
			print(text)
			return ""
		subscriber_server.register_function(notify)

		broadcaster = xmlrpc.client.ServerProxy('http://localhost:8001')
		print(broadcaster.register_subscriber('http://localhost:' + sys.argv[1]))

		# Run the server's main loop
		subscriber_server.serve_forever()
