import xmlrpc.client

# Getting server in "http://localhost:8000"
name_server = xmlrpc.client.ServerProxy('http://localhost:8000')

insult_service = name_server.get_insult_workers()

insults = ["papanatas", "bobo", "estupido", "bobete"]

i = 0
for i < 3:
	for insult_service_worker_uri in insult_service:
		insult_service_worker = xmlrpc.client.ServerProxy(insult_service_worker_uri)
		insult_service_worker.add_insult(insults[i])
	i = i + 1
