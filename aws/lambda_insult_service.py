import pika
import threading
import time
import redis
import json

# Insert here the IP of the EC2 instance
ec2_ip = '54.165.250.164'
INSULT_QUEUE = "insult_queue"
END_PETITION_QUEUE = "end_petition_queue_"

def create_connection():
	credentials = pika.PlainCredentials('user', 'password123')
	connection = pika.BlockingConnection(
		pika.ConnectionParameters(
			host=ec2_ip,
			credentials=credentials
		)
	)

def callback(ch, method, properties, body, stop_event):
	print(f"Received stop signal: {body}")
	stop_event.set()
	ch.basic_ack(delivery_tag=method.delivery_tag)  # Acknowledge the message to remove it from the queue
	ch.stop_consuming()

def wait_for_stop_signal(stop_event, lambda_id):

	queue = END_PETITION_QUEUE + str(lambda_id)

	connection = create_connection()
	channel = connection.channel()
	channel.queue_declare(queue=queue, durable=True)

	channel.basic_consume(
		queue=queue,
		on_message_callback=lambda ch, method, properties, body: callback(ch, method, properties, body, stop_event)
	)
	print(f"Waiting for stop signal on queue '{queue}'...")
	channel.start_consuming()
	connection.close()


def consume_insults(stop_event, redis_server):
	connection = create_connection()
	channel = connection.channel()
	channel.queue_declare(queue=INSULT_QUEUE, durable=True)

	# Wrap callback to include stop_event
	def on_message(ch, method, properties, body):

		# Obtain the msg
		message_str = body.decode('utf-8')
	
		# Parse JSON string to dict
		order = json.loads(message_str)
	
		print("Processing order:", order)
	
		insult = order.get('insult')

		# Add insult to redis if not there
		if not redis_server.sismember("insults", insult):
			redis_server.sadd("insults", insult)
		if stop_event.is_set():
			print("Stop event set, stopping insult consumer.")
			ch.stop_consuming()

	channel.basic_consume(queue=INSULT_QUEUE, on_message_callback=on_message)

	print("Starting insult consumer, waiting for messages...")
	channel.start_consuming()
	print("Insult consumer stopped.")
	connection.close()

def lambda_handler(event, context):

	lambda_id = event.get('param', 0)

	redis_server = redis.Redis(host=ec2_ip, port=6379, decode_responses=True)

	# Thread that waits if the lambda needs to be scaled down
	stop_event = threading.Event()
	threading.Thread(target=wait_for_stop_signal, args=(stop_event, lambda_id,)).start()

	consume_insults(stop_event, redis_server)

	return {
		"statusCode": 200,
		"body": "stopped by signal"
	}
