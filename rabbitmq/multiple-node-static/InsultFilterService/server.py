import redis
import logging
import json
import pika
from datetime import datetime, timezone
import traceback

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(message)s",
    handlers=[
        logging.FileHandler("insult_filter_service.log", mode="a"),
        logging.StreamHandler()
    ]
)

class InsultFilterService:
    def __init__(self):
        self.r = redis.Redis(host='localhost', port=6379, decode_responses=True)

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

    def add_text(self, input_texts):
        if isinstance(input_texts, str):
            input_texts = [input_texts]

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
            else:
                logging.info(f"Filtered text already exists: {filtered}")

    def start_rabbitmq_consumer(self):
        try:
            credentials = pika.PlainCredentials("ar", "sar")
            parameters = pika.ConnectionParameters("localhost", credentials=credentials)
            logging.info("Connecting to RabbitMQ...")
            connection = pika.BlockingConnection(parameters)
            channel = connection.channel()

            channel.queue_declare(queue="text_queue", durable=True)
            logging.info("Queue declared: text_queue")

            def callback(ch, method, properties, body):
                try:
                    data = json.loads(body)
                    text = data.get("text")
                    if text:
                        self.add_text(text)
                        ch.basic_ack(delivery_tag=method.delivery_tag)
                        logging.info(f"Text processed: {text}")
                except Exception:
                    logging.error("Error processing message:")
                    traceback.print_exc()

            channel.basic_qos(prefetch_count=1)
            channel.basic_consume(queue="text_queue", on_message_callback=callback)
            logging.info("Waiting for messages on text_queue...")
            channel.start_consuming()

        except Exception:
            logging.error("Fatal error in RabbitMQ consumer:")
            traceback.print_exc()

if __name__ == "__main__":
    service = InsultFilterService()
    service.start_rabbitmq_consumer()
