import pika
import redis
import time
import random
import json
import logging

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(message)s",
    handlers=[
        logging.FileHandler("notifier_rabbitmq.log", mode="a"),
        logging.StreamHandler()
    ]
)

def broadcast_loop():
    r = redis.Redis(host='localhost', port=6379, decode_responses=True)
    
    credentials = pika.PlainCredentials("ar", "sar")
    parameters = pika.ConnectionParameters("localhost", credentials=credentials)
    connection = pika.BlockingConnection(parameters)
    channel = connection.channel()

    channel.exchange_declare(exchange="insult_broadcast", exchange_type="fanout")

    while True:
        insults = list(r.smembers("insults"))
        if not insults:
            logging.info("No hay insultos disponibles.")
        else:
            insult = random.choice(insults)
            message = json.dumps({"insult": insult})
            channel.basic_publish(exchange="insult_broadcast", routing_key="", body=message)
            logging.info(f"Enviado broadcast: {insult}")
        time.sleep(5)

if __name__ == "__main__":
    broadcast_loop()