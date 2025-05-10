# Is this even used? For what reason?

import subprocess
import time

try:
	subprocess.Popen(["redis-server"])
	time.sleep(1)  # Esperar que arranque
	print("Redis iniciado.")
except FileNotFoundError:
	print("redis-server no encontrado. ¿Está instalado y en PATH?")
