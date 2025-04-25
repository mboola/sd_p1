import Pyro4
from Config import config

# Obtener proxy del servidor
main_server = Pyro4.Proxy(f"PYRONAME:{config.CONFIG_SERVER_NAME}@{config.HOSTNAME}:{config.NAMESERVER_PORT}")

# ID de cliente ficticio
client_id = "client_1"

# Solicitar un worker de insultos
worker_uri = main_server.get_insult_worker(client_id)
print(f"Worker asignado: {worker_uri}")

# Simular uso del worker...
input("Presiona Enter para liberar el worker...")

# Liberar el worker
main_server.free_insult_worker(worker_uri)
print("Worker liberado.")
