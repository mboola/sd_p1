import pika
import time
import redis
import random

# Connect to Redis
redis_server = redis.Redis(host='localhost', port=6379, db=0, decode_responses=True)
insult_list = "insult_list"

# Connect to RabbitMQ
connection = pika.BlockingConnection(pika.ConnectionParameters('localhost'))
channel = connection.channel()

exchange_name = 'event_queue'
channel.exchange_declare(exchange=exchange_name, exchange_type='fanout')

while True:
	insults = redis_server.lrange(insult_list, 0, -1)
	if len(insults) > 0:
		insult = random.choice(insults)
		channel.basic_publish(exchange=exchange_name, routing_key='', body=insult)
	time.sleep(5)
