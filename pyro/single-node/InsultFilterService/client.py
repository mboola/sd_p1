from Pyro4 import Proxy

# Conectar con el servidor
remote = Proxy("PYRO:InsultFilterService@localhost:4040")

# Enviar texto y insulto:
text = "hola"
filtered = remote.add_text(text)
print("Texto filtrado: ", filtered)

text = "idiota"
filtered = remote.add_text(text)
print("Texto filtrado: ", filtered)

# Obtener todos los resultados filtrados
results = remote.get_texts()
print("Lista de textos filtrados:", results)


import Pyro4
from config import config

# Obtener proxy del servidor
main_server = Pyro4.Proxy(f"PYRONAME:MainServer@{config.HOSTNAME}:{config.NAMESERVER_PORT}")

# ID de cliente ficticio
client_id = "cliente_123"

# Solicitar un worker de insultos
worker_uri = main_server.get_insult_worker(client_id)
print(f"Worker asignado: {worker_uri}")

# Simular uso del worker...
input("Presiona Enter para liberar el worker...")

# Liberar el worker
main_server.free_insult_worker(worker_uri)
print("Worker liberado.")
