import subprocess
import time
import os

BASE_DIR = os.path.abspath(os.path.dirname(__file__))

def lanzar(nombre, comando, espera=1):
    print(f" Iniciando: {nombre}")
    proceso = subprocess.Popen(comando, shell=True)
    time.sleep(espera)
    return proceso

def main():
    procesos = []

    try:
        # 0. Name Server
        procesos.append(lanzar("NameServer", "pyro4-ns"))

        # 1. Redis
        procesos.append(lanzar("Redis", f"python3 {BASE_DIR}/RedisServer.py"))

        # 2. InsultService
        procesos.append(lanzar("InsultService", f"python3 {BASE_DIR}/InsultService/server.py"))

        # 3. InsultFilterService
        procesos.append(lanzar("InsultFilterService", f"python3 {BASE_DIR}/InsultFilterService/server.py"))

        # 4. Notifier
        procesos.append(lanzar("Notifier", f"python3 {BASE_DIR}/Notifier/notifier.py"))

        # 5. Subscriber
        procesos.append(lanzar("Subscriber", f"python3 {BASE_DIR}/Notifier/subscriber.py"))

        # 6. Client InsultService
        procesos.append(lanzar("Client InsultService", f"python3 {BASE_DIR}/InsultService/client.py"))

        # 7. Client InsultFilterService
        procesos.append(lanzar("Client InsultFilterService", f"python3 {BASE_DIR}/InsultFilterService/client.py"))

        print("\n Todos los procesos han sido lanzados.")
        print(" Pulsa Ctrl+C para detener manualmente.")

        # Espera indefinida (los procesos siguen corriendo)
        while True:
            time.sleep(1)

    except KeyboardInterrupt:
        print("\n Deteniendo todos los procesos...")
        for p in procesos:
            p.terminate()
        print(" Finalizado.")

if __name__ == "__main__":
    main()
