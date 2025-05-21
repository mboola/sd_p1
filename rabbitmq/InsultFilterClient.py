import pika
import sys
import json

text_list = [
	"Eres un papanatas!",
	"Tremendo bobo",
	"Como puedes ser tan estupido, estupido?",
	"bobete bobete bobo bobete"
]

texts_queue = "texts_queue"

petitions = int(sys.argv[1])

# Connect to RabbitMQ
parameters = pika.ConnectionParameters("localhost")
connection = pika.BlockingConnection(parameters)
channel = connection.channel()

# Declare the queue (creates if not exists)
channel.queue_declare(queue=texts_queue)

for i in range(petitions):
	message = json.dumps({"text": text_list[i % 4]})
	channel.basic_publish(exchange='', routing_key=texts_queue, body=message)

connection.close()
