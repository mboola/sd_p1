import Pyro4
import redis
import logging
import sys
from datetime import datetime, timezone
import threading
import pika
import json

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(message)s",
    handlers=[
        logging.FileHandler("insult_filter_service.log", mode="a"),
        logging.StreamHandler()
    ]
)

@Pyro4.behavior(instance_mode="single")
class InsultFilterService:
    def __init__(self):
        self.r = redis.Redis(host='localhost', port=6379, decode_responses=True)
        self.subscribers = []

    def get_insults_list(self):
        return self.r.smembers("insults")

    def filter_text(self, text):
        insults_set = self.get_insults_list()
        words = text.split()
        censored = [
            "CENSORED" if word.lower() in insults_set else word
            for word in words
        ]
        return " ".join(censored)

    @Pyro4.expose
    def add_text(self, input_texts):
        if isinstance(input_texts, str):
            input_texts = [input_texts]

        results = []
        for text in input_texts:
            text = text.lower()
            filtered = self.filter_text(text)
            values = self.r.hvals("filtered_texts")
            already_exists = any(filtered == v.split("|")[0] for v in values)

            if not already_exists:
                timestamp = datetime.now(timezone.utc).isoformat()
                next_id = self.r.incr("filtered_texts_id")
                self.r.hset("filtered_texts", next_id, f"{filtered}|{timestamp}")
                logging.info(f"Filtered text added: {filtered}")
                results.append(f"Text registered: {filtered} (UTC: {timestamp})")
            else:
                logging.info(f"Text already registered: {filtered}")
                results.append(f"Text already registered: {filtered}")
        return results

    @Pyro4.expose
    def get_texts(self):
        raw = self.r.hgetall("filtered_texts")
        return [{ "id": k, "text": v.split("|")[0], "timestamp": v.split("|")[1] } for k, v in raw.items()]

    def start_rabbitmq_consumer(self):
        def callback(ch, method, properties, body):
            try:
                data = json.loads(body)
                text = data.get("text")
                if text:
                    self.add_text(text)
                    ch.basic_ack(delivery_tag=method.delivery_tag)
                    logging.info(f"✅ Text consumed from queue: {text}")
            except Exception as e:
                logging.error(f"❌ Error processing message: {e}")

        def run():
            connection = pika.BlockingConnection(pika.ConnectionParameters("localhost"))
            channel = connection.channel()
            channel.queue_declare(queue="text_queue", durable=True)
            channel.basic_qos(prefetch_count=1)
            channel.basic_consume(queue="text_queue", on_message_callback=callback)
            logging.info("🎧 Listening on RabbitMQ queue: text_queue")
            channel.start_consuming()

        threading.Thread(target=run, daemon=True).start()


def main():
    port = int(sys.argv[1])  # >= 50152
    name = sys.argv[2]       # e.g. InsultFilterService_0

    obj = InsultFilterService()
    obj.start_rabbitmq_consumer()

    daemon = Pyro4.Daemon(port=port)
    ns = Pyro4.locateNS()
    uri = daemon.register(obj)
    ns.register(name, uri)
    logging.info(f"{name} registered at {uri}")
    daemon.requestLoop()
