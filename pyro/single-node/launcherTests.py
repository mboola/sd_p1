import subprocess
import time
import os
import sys
import redis

BASE_DIR = os.path.abspath(os.path.dirname(__file__))

def launch(name, command, wait=1):
    print(f" Iniciando: {name}")
    process = subprocess.Popen(command, shell=True)
    time.sleep(wait)
    return process

def main():
    processes = []

    try:
        number_petitions_insult = int(sys.argv[1])
        number_petitions_text = int(sys.argv[2])

        # 0. Name Server
        processes.append(launch("NameServer", "pyro4-ns"))

        # 1. Redis
        processes.append(launch("Redis", f"python3 {BASE_DIR}/RedisServer.py"))

        # 2. InsultService
        processes.append(launch("InsultService", f"python3 {BASE_DIR}/InsultService/server.py"))

        # 3. InsultFilterService
        processes.append(launch("InsultFilterService", f"python3 {BASE_DIR}/InsultFilterService/server.py"))

        # 4. Notifier
        processes.append(launch("Notifier", f"python3 {BASE_DIR}/Notifier/notifier.py"))

        # 5. Subscriber
        processes.append(launch("Subscriber", f"python3 {BASE_DIR}/Notifier/subscriber.py"))

        # 6. Test InsultService
        processes.append(launch("Test InsultService", f"python3 {BASE_DIR}/tests/test_InsultService.py {number_petitions_insult}"))

        # 7. Test InsultFilterService
        processes.append(launch("Test InsultFilterService", f"python3 {BASE_DIR}/tests/test_InsultFilterService.py {number_petitions_text}"))

        print("\n Todos los procesos han sido lanzados.")
        print(" Pulsa Ctrl+C para detener manualmente.")

        # Espera indefinida (los procesos siguen corriendo)
        while True:
            time.sleep(1)

    except KeyboardInterrupt:
        print("\n Deteniendo todos los procesos...")
        for p in processes:
            p.terminate()

        print("🧹 Killing NameServer...")
        subprocess.call("pkill -f pyro4-ns", shell=True)

        print(" Limpiando Redis...")
        try:
            r = redis.Redis(host='localhost', port=6379, decode_responses=True)

            insults_count = r.scard("insults")
            texts_count = r.hlen("filtered_texts")
            text_id = r.get("filtered_texts_id")

            r.delete("insults", "filtered_texts", "filtered_texts_id")

            print(f" ELIMINAR insults: {insults_count} elementos eliminados.")
            print(f" ELIMINAR filtered_texts: {texts_count} textos eliminados.")
            print(f" ELIMINAR filtered_texts_id: {text_id} contador eliminado.")

        except Exception as e:
            print(f" ERROR al borrar claves en Redis: {e}")

        print(" Finalizado.")

if __name__ == "__main__":
    main()
