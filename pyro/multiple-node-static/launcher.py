import subprocess
import time
import os
import redis
import sys

BASE_DIR = os.path.abspath(os.path.dirname(__file__))

def launch(name, command, wait_time=1):
    print(f"🚀 Iniciando: {name}")
    process = subprocess.Popen(command, shell=True)
    time.sleep(wait_time)
    return process

def main():
    processes = []

    try:
        number_insult_services = int(sys.argv[1])
        number_filter_services = int(sys.argv[2])
        number_petitions_insult = int(sys.argv[3])
        number_petitions_text = int(sys.argv[4])

        # 0. Name Server
        processes.append(launch("NameServer", "pyro4-ns"))

        # 1. Redis
        processes.append(launch("Redis", f"python3 {BASE_DIR}/RedisServer.py"))

        # 2. Multiple instancias de InsultService
        base_port_insult = 49152
        for i in range(number_insult_services):
            port = base_port_insult + i
            name = f"InsultService_{i}"
            cmd = f"python3 InsultService/server.py {port} {name}"
            processes.append(launch(name, cmd))

        # 3. Multiple instancias de InsultFilterService
        base_port_filter = 50152
        for i in range(number_filter_services):
            port = base_port_filter + i
            name = f"InsultFilterService_{i}"
            cmd = f"python3 InsultFilterService/server.py {port} {name}"
            processes.append(launch(name, cmd))

        # 4. Notifier
        processes.append(launch("Notifier", f"python3 {BASE_DIR}/Notifier/notifier.py"))

        # 5. Subscriber
        processes.append(launch("Subscriber", f"python3 {BASE_DIR}/Notifier/subscriber.py"))

        # 6. Test InsultService
        processes.append(launch("Test InsultService", f"python3 {BASE_DIR}/InsultService/test_InsultService.py {number_insult_services} {number_filter_services} {number_petitions_insult} {number_petitions_text}"))

        # 7. Test InsultFilterService
        processes.append(launch("Test InsultFilterService", f"python3 {BASE_DIR}/InsultFilterService/test_InsultFilterService.py {number_insult_services} {number_filter_services} {number_petitions_insult} {number_petitions_text}"))

        print("OK Todas las instancias están en ejecución.")
        print("STOP Ctrl+C para detener todo.")
        while True:
            time.sleep(1)

    except KeyboardInterrupt:
        print(" Deteniendo procesos...")
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

        print(" COMPLETADO.")

if __name__ == "__main__":
    main()
