import subprocess
import time
import os
import sys
import redis
import socket
import Pyro4
import signal

BASE_DIR = os.path.abspath(os.path.dirname(__file__))


def launch(name, command, wait=1):
    print(f" Iniciando: {name}")
    process = subprocess.Popen(command, shell=True)
    time.sleep(wait)
    return process


def is_redis_running(host='localhost', port=6379):
    try:
        r = redis.Redis(host=host, port=port)
        return r.ping()
    except Exception:
        return False


def is_nameserver_running():
    try:
        Pyro4.locateNS()
        return True
    except Exception:
        return False
    

def main():
    processes = []

    try:
        number_petitions_insult = int(sys.argv[1])
        number_petitions_text = int(sys.argv[2])

        # 0. Name Server
        if not is_nameserver_running():
            processes.append(launch("NameServer", "pyro4-ns"))
        else:
            print(" NameServer ya en ejecución, omitiendo lanzamiento.")

        # 1. Redis
        if not is_redis_running():
            processes.append(launch("Redis", f"python3 {BASE_DIR}/RedisServer.py"))
        else:
            print(" Redis ya en ejecución, omitiendo lanzamiento.")

        # 2. InsultService
        processes.append(launch("InsultService", f"python3 {BASE_DIR}/InsultService/server.py"))

        # 3. InsultFilterService
        processes.append(launch("InsultFilterService", f"python3 {BASE_DIR}/InsultFilterService/server.py"))

        # 4. Test InsultService
        processes.append(launch("Test InsultService", f"python3 {BASE_DIR}/tests/test_InsultService.py {number_petitions_insult}"))
        
        # 5. Test InsultFilterService
        processes.append(launch("Test InsultFilterService", f"python3 {BASE_DIR}/tests/test_InsultFilterService.py {number_petitions_text}"))

        print("\n Todos los procesos han sido lanzados.")
        print(" Pulsa Ctrl+C para detener manualmente.")
        os.kill(os.getpid(), signal.SIGINT)
        while True:
            time.sleep(1)

    except KeyboardInterrupt:
        print("\n Deteniendo todos los procesos...")
        for p in processes:
            try:
                p.terminate()
            except Exception:
                pass

        # Kill NameServer if launched by this script
        if not is_nameserver_running():
            print("🧹 Killing NameServer...")
            subprocess.call("pkill -f pyro4-ns", shell=True)

        # Clean Redis if launched
        print("🧹 Limpiando Redis si lanzado por este script...")
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
