import subprocess
import time

def iniciar_redis():
    try:
        subprocess.Popen(["redis-server"])
        time.sleep(1)  # Esperar que arranque
        print("✅ Redis iniciado.")
    except FileNotFoundError:
        print("❌ redis-server no encontrado. ¿Está instalado y en PATH?")

if __name__ == "__main__":
    iniciar_redis()
