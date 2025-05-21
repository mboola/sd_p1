import redis
import pika
import re
import sys

petitions = int(sys.argv[1])

# Connect to Redis
server = redis.Redis(host='localhost', port=6379, db=0, decode_responses=True)

# RabbitMQ setup
connection = pika.BlockingConnection(pika.ConnectionParameters('localhost'))
channel = connection.channel()

insult_list = "insult_list"
texts_queue = "texts_queue"
result_queue = "filtered_texts"
end_condition_queue = "end_condition_queue"

# Declare rabbitmq queue
channel.queue_declare(queue=texts_queue)
channel.queue_declare(queue=result_queue)
channel.queue_declare(queue=end_condition_queue)


def callback(ch, method, properties, body):
	new_text = body.decode()

	banned_words = server.lrange(insult_list, 0, -1)

	# Filter banned words
	for banned_word in banned_words:
		new_text = re.sub(banned_word, "CENSORED", new_text, flags=re.IGNORECASE)
	server.rpush(result_queue, new_text)
	length = server.llen(result_queue)
	if (length >= petitions):
			channel.basic_publish(exchange='', routing_key=end_condition_queue, body="Ended!")
			print("End condition reached. Sent 'Ended!' notification.")
			# Optionally stop consuming to end program:
			ch.stop_consuming()
	

channel.basic_consume(queue=texts_queue, on_message_callback=callback, auto_ack=True)

channel.start_consuming()

connection.close()
