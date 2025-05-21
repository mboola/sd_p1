import pika
import time

# Connect to RabbitMQ
connection = pika.BlockingConnection(pika.ConnectionParameters('localhost'))
channel = connection.channel()

# Declare (create) a queue
queue_name = 'end_condition_queue'
channel.queue_declare(queue=queue_name)

# Start timing
start_time = time.time()

def callback(ch, method, properties, body):
    # Stop consuming after first message
    ch.stop_consuming()

# Subscribe / consume messages from the queue
channel.basic_consume(queue=queue_name, on_message_callback=callback, auto_ack=True)

channel.start_consuming()

# Done
print(f"Total time: {time.time() - start_time:.2f} seconds")

connection.close()
