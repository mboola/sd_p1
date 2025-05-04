import time
import pika
import json

N = 1000

def main():
    credentials = pika.PlainCredentials("ar", "sar")
    parameters = pika.ConnectionParameters("localhost", credentials=credentials)
    connection = pika.BlockingConnection(parameters)
    channel = connection.channel()
    channel.queue_declare(queue="text_queue", durable=True)

    print(f"📤 Sending {N} texts to text_queue...")

    start = time.time()
    for i in range(N):
        text = f"This is a text with insult_{i}"
        message = json.dumps({"text": text})
        channel.basic_publish(
            exchange='',
            routing_key='text_queue',
            body=message,
            properties=pika.BasicProperties(delivery_mode=2)
        )
    end = time.time()
    connection.close()

    total_time = end - start
    throughput = N / total_time

    results = (
        f"TEST RABBITMQ: InsultFilterService\n"
        f"Messages: {N}\n"
        f"Total time: {total_time:.4f} seconds\n"
        f"Throughput: {throughput:.2f} msg/sec\n"
    )

    print(results)
    with open(f"results_rabbitmq_insultfilterservice_{N}.txt", "w") as f:
        f.write(results)

if __name__ == "__main__":
    main()
