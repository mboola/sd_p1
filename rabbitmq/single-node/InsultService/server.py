import redis
import json
import pika
import logging
import sys
from datetime import datetime
import traceback

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(message)s",
    handlers=[
        logging.FileHandler("insult_service.log", mode="a"),
        logging.StreamHandler()
    ]
)

class InsultService:
    def __init__(self, end_condition_target=None):
        self.r = redis.Redis(host='localhost', port=6379, decode_responses=True)
        self.end_condition_target = end_condition_target

    def add_insult(self, insult_or_list):
        if isinstance(insult_or_list, str):
            insult_or_list = [insult_or_list]

        for insult in insult_or_list:
            insult = insult.lower()
            if not self.r.sismember("insults", insult):
                self.r.sadd("insults", insult)
                current_total = self.r.scard("insults")

                # Publicar si alcanzamos el total esperado
                if self.end_condition_target and current_total == self.end_condition_target:
                    self.r.publish("end_condition_insults", "done")

    def start(self):
        try:
            credentials = pika.PlainCredentials("ar", "sar")
            parameters = pika.ConnectionParameters("localhost", credentials=credentials)
            connection = pika.BlockingConnection(parameters)
            channel = connection.channel()
            channel.queue_declare(queue="insult_queue", durable=True)

            def callback(ch, method, properties, body):
                try:
                    data = json.loads(body)
                    insult = data.get("insult")
                    if insult:
                        self.add_insult(insult)
                        ch.basic_ack(delivery_tag=method.delivery_tag)
                        logging.info(f"Insult processed: {insult}")
                except Exception:
                    logging.error("Error processing message:")
                    traceback.print_exc()

            channel.basic_qos(prefetch_count=1)
            channel.basic_consume(queue="insult_queue", on_message_callback=callback)
            logging.info("[READY] Waiting for insults...")
            channel.start_consuming()

        except Exception:
            logging.error("[Fatal] RabbitMQ consumer failure:")
            traceback.print_exc()

def main():
    
    n_pis = int(sys.argv[1]) if len(sys.argv) > 1 else None
    service = InsultService(end_condition_target=n_pis)
    service.start()

if __name__ == "__main__":
    main()