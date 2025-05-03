import Pyro4
import redis
import sys
import logging
import threading
import pika
import json

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(message)s",
    handlers=[
        logging.FileHandler("insult_service.log", mode="a"),
        logging.StreamHandler()
    ]
)

@Pyro4.behavior(instance_mode="single")
class InsultService:
    def __init__(self):
        self.r = redis.Redis(host='localhost', port=6379, decode_responses=True)

    @Pyro4.expose
    def add_insult(self, insult_or_list):
        if isinstance(insult_or_list, str):
            insult_or_list = [insult_or_list]

        results = []
        for insult in insult_or_list:
            insult = insult.lower()
            if not self.r.sismember("insults", insult):
                self.r.sadd("insults", insult)
                logging.info(f"Insult added: {insult}")
                results.append(f"Insult registered: {insult}")
            else:
                logging.info(f"Insult already exists: {insult}")
                results.append(f"Insult already registered: {insult}")
        return results

    @Pyro4.expose
    def get_insults(self):
        return list(self.r.smembers("insults"))

    def start_rabbitmq_consumer(self):
        def callback(ch, method, properties, body):
            try:
                data = json.loads(body)
                insult = data.get("insult")
                if insult:
                    self.add_insult(insult)
                    ch.basic_ack(delivery_tag=method.delivery_tag)
                    logging.info(f"✅ Insult consumed from queue: {insult}")
            except Exception as e:
                logging.error(f"❌ Error processing message: {e}")

        def run():
            connection = pika.BlockingConnection(pika.ConnectionParameters("localhost"))
            channel = connection.channel()
            channel.queue_declare(queue="insult_queue", durable=True)
            channel.basic_qos(prefetch_count=1)
            channel.basic_consume(queue="insult_queue", on_message_callback=callback)
            logging.info("🎧 Listening on RabbitMQ queue: insult_queue")
            channel.start_consuming()

        threading.Thread(target=run, daemon=True).start()

def main():
    port = int(sys.argv[1])  # >= 49152
    name = sys.argv[2]       # e.g. InsultService_0

    obj = InsultService()
    obj.start_rabbitmq_consumer()

    daemon = Pyro4.Daemon(port=port)
    ns = Pyro4.locateNS()
    uri = daemon.register(obj)
    ns.register(name, uri)
    logging.info(f"{name} registered at {uri}")
    daemon.requestLoop()
