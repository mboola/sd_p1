import xmlrpc.client
import time

# Getting server in "http://localhost:8000"
name_server = xmlrpc.client.ServerProxy('http://localhost:8000')

insult_service_workers_uri = name_server.get_insult_workers()

insults = ["papanatas", "bobo", "estupido", "bobete"]

i = 0
j = 0
n_workers = len(insult_service_workers_uri)
for i in range(4):
	print(f"Adding '{insults[i]}' to Insult Service URI '{insult_service_workers_uri[j]}'!")
	insult_service_worker = xmlrpc.client.ServerProxy(insult_service_workers_uri[j])
	print(insult_service_worker.add_insult(insults[i]))
	if (j + 1 == n_workers):
		j = 0
	else:
		j = j + 1
	time.sleep(1)
