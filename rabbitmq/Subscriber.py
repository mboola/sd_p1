import pika

channel_name = "event_queue"  # RabbitMQ uses queues instead of channels

# Connect to RabbitMQ
connection = pika.BlockingConnection(pika.ConnectionParameters('localhost'))
channel = connection.channel()

# Declare the queue (create if not exists)
channel.queue_declare(queue=channel_name)

print(f"Subscribed to {channel_name}, waiting for messages...")

def callback(ch, method, properties, body):
    print(f"Received: {body.decode()}")

# Start consuming messages from the queue
channel.basic_consume(queue=channel_name, on_message_callback=callback, auto_ack=True)
channel.start_consuming()
