import random
from xmlrpc.server import SimpleXMLRPCServer
from xmlrpc.server import SimpleXMLRPCRequestHandler

# Restrict to a particular path
class RequestHandler(SimpleXMLRPCRequestHandler):
	rpc_paths = ('/RPC2',)

insults = ["Pig!"]

# Create server
with SimpleXMLRPCServer(('localhost', 8000),
						requestHandler = RequestHandler) as server:

	name_server = xmlrpc.client.ServerProxy('http://localhost:8000')

	server.register_introspection_functions()

	def add_insult(insult):
		client.chn
		insults.append(insult)
		return "Insult '" + insult + "' added."
	server.register_function(add_insult)

	def get_insults():
		return insults
	server.register_function(get_insults)

	def insult_me():
		return random.choice(insults)
	server.register_function(insult_me)

	# Run the server's main loop
	server.serve_forever()
