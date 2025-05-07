#python3 launcher.py <number_insult_services> <number_filter_services> <number_insults> <number_texts_to_filter>

import subprocess
import time
import os
import redis
import sys

BASE_DIR = os.path.abspath(os.path.dirname(__file__))

def launch(name, command, wait_time=1):
    print(f"🚀 Launching: {name}")
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

        # 2. RabbitMQ (optional - you can skip this if running as a service)
        # processes.append(launch("RabbitMQ", "rabbitmq-server"))

        # 3. Multiple InsultService instances
        base_port_insult = 49152
        for i in range(number_insult_services):
            port = base_port_insult + i
            name = f"InsultService_{i}"
            cmd = f"python3 {BASE_DIR}/InsultService/server.py {port} {name}"
            processes.append(launch(name, cmd))

        # 4. Multiple InsultFilterService instances
        base_port_filter = 50152
        for i in range(number_filter_services):
            port = base_port_filter + i
            name = f"InsultFilterService_{i}"
            cmd = f"python3 {BASE_DIR}/InsultFilterService/server.py {port} {name}"
            processes.append(launch(name, cmd))

        # 5. Notifier and Subscriber
        processes.append(launch("Notifier", f"python3 {BASE_DIR}/Notifier/notifier.py"))
        processes.append(launch("Subscriber", f"python3 {BASE_DIR}/Notifier/subscriber.py"))

        # 6. RabbitMQ clients (to send messages)
        #processes.append(launch("Client RabbitMQ - Insults", f"python3 {BASE_DIR}/InsultService/client.py"))
        #processes.append(launch("Client RabbitMQ - Texts", f"python3 {BASE_DIR}/InsultFilterService/client.py"))

        # 7. Tests
        processes.append(launch("Test RabbitMQ - Insults", f"python3 {BASE_DIR}/InsultService/test_insultService.py {number_insult_services} {number_filter_services} {number_petitions_insult} {number_petitions_text}"))
        processes.append(launch("Test RabbitMQ - Texts", f"python3 {BASE_DIR}/InsultFilterService/test_insultFilterService.py {number_insult_services} {number_filter_services} {number_petitions_insult} {number_petitions_text}"))

        print("✅ All services are running.")
        print("🛑 Press Ctrl+C to stop everything.")
        while True:
            time.sleep(1)

    except KeyboardInterrupt:
        print("🧹 Stopping all processes...")
        for p in processes:
            p.terminate()

        print("🧹 Killing NameServer...")
        subprocess.call("pkill -f pyro4-ns", shell=True)

        print("🧹 Cleaning Redis keys...")
        try:
            r = redis.Redis(host='localhost', port=6379, decode_responses=True)
            insults_count = r.scard("insults")
            texts_count = r.hlen("filtered_texts")
            text_id = r.get("filtered_texts_id")

            r.delete("insults", "filtered_texts", "filtered_texts_id")

            print(f"🗑️ insults deleted: {insults_count}")
            print(f"🗑️ filtered_texts deleted: {texts_count}")
            print(f"🗑️ filtered_texts_id removed: {text_id}")
        except Exception as e:
            print(f"⚠️ Redis clean-up error: {e}")

        print("👋 Done.")

if __name__ == "__main__":
    main()
