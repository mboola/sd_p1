import xmlrpc.client

# Getting server in "http://localhost:8000"
server = xmlrpc.client.ServerProxy('http://localhost:8000')

# Using functions defined inside server
print(server.add_insult("Stupid!"))
print(server.get_insults())
print(server.insult_me())

# Print list of all available methods
print(server.system.listMethods())
