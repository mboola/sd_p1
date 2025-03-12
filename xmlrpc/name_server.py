from xmlrpc.server import SimpleXMLRPCServer
from xmlrpc.server import SimpleXMLRPCRequestHandler

# Restrict to a particular path
class RequestHandler(SimpleXMLRPCRequestHandler):
	rpc_paths = ('/RPC2',)

servers = []

# Create server
with SimpleXMLRPCServer(('localhost', 8000),
						requestHandler = RequestHandler) as name_server:

	def add_server(server):
		servers.append(server)
		return "Server '" + server + "' added."
	name_server.register_function(add_server)

	def get_servers():
		return servers
	name_server.register_function(get_servers)

	# Run the server's main loop
	name_server.serve_forever()
