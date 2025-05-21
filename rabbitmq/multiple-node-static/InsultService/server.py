import redis
import logging
import json
import pika
import traceback

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(message)s",
    handlers=[
        logging.FileHandler("insult_service.log", mode="a"),
        logging.StreamHandler()
    ]
)

def add_insult(insult_or_list, redis_conn):
    if isinstance(insult_or_list, str):
        insult_or_list = [insult_or_list]

    for insult in insult_or_list:
        insult = insult.lower()
        if not redis_conn.sismember("insults", insult):
            redis_conn.sadd("insults", insult)
            redis_conn.publish("insults_channel", insult)  # <- 🔔 Notifica por pub/sub
            logging.info(f"Insult added: {insult}")
        else:
            logging.info(f"Insult already exists: {insult}")

def main():
    try:
        r = redis.Redis(host='localhost', port=6379, decode_responses=True)
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
                    add_insult(insult, r)
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

if __name__ == "__main__":
    main()