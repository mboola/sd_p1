import pika
import json
import sys

text_list = ["Eres un papanatas!", "Tremendo bobo", "Como puedes ser tan estupido, estupido?", "bobete bobete bobo bobete"]

petitions = int(sys.argv[1])

#credentials = pika.PlainCredentials("ar", "sar")
parameters = pika.ConnectionParameters("localhost")
connection = pika.BlockingConnection(parameters)
channel = connection.channel()
channel.queue_declare(queue="text_queue", durable=True)

for i in range(petitions):
    message = json.dumps({"text": text_list[i % 4]})
    channel.basic_publish(
        exchange='',
        routing_key='text_queue',
        body=message,
        properties=pika.BasicProperties(delivery_mode=2)
    )
    
connection.close()
