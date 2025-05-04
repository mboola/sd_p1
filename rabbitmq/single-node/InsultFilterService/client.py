import pika
import json

def publish_texts(text_list):
    credentials = pika.PlainCredentials("ar", "sar")
    parameters = pika.ConnectionParameters("localhost", credentials=credentials)
    connection = pika.BlockingConnection(parameters)


    channel = connection.channel()

    channel.queue_declare(queue="text_queue", durable=True)

    if isinstance(text_list, str):
        text_list = [text_list]

    for text in text_list:
        message = json.dumps({"text": text})
        channel.basic_publish(
            exchange='',
            routing_key='text_queue',
            body=message,
            properties=pika.BasicProperties(delivery_mode=2)
        )
        print(f"📤 Sent text: {text}")

    connection.close()

if __name__ == "__main__":
    texts = [
        "You're such a clown",
        "That was a moron move",
        "Twit behavior again?",
        "What a loser you are"
    ]
    publish_texts(texts)
