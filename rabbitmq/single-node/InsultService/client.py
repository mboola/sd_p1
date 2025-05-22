import pika
import json

def publish_insults(insult_list):
    credentials = pika.PlainCredentials("ar", "sar")
    parameters = pika.ConnectionParameters("localhost", credentials=credentials)
    connection = pika.BlockingConnection(parameters)
    channel = connection.channel()

    channel.queue_declare(queue="insult_queue", durable=True)

    if isinstance(insult_list, str):
        insult_list = [insult_list]

    for insult in insult_list:
        message = json.dumps({"insult": insult})
        channel.basic_publish(
            exchange='',
            routing_key='insult_queue',
            body=message,
            properties=pika.BasicProperties(delivery_mode=2)
        )
        print(f"📤 Sent insult: {insult}")

    connection.close()

if __name__ == "__main__":
    insults = ["moron", "twit", "loser", "clown"]
    publish_insults(insults)
