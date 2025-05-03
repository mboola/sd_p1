import time
import pika
import json

N = 1000

def main():
    connection = pika.BlockingConnection(pika.ConnectionParameters("localhost"))
    channel = connection.channel()
    channel.queue_declare(queue="insult_queue", durable=True)

    print(f"📤 Sending {N} insults to insult_queue...")

    start = time.time()
    for i in range(N):
        insult = f"insult_{i}"
        message = json.dumps({"insult": insult})
        channel.basic_publish(
            exchange='',
            routing_key='insult_queue',
            body=message,
            properties=pika.BasicProperties(delivery_mode=2)
        )
    end = time.time()
    connection.close()

    total_time = end - start
    throughput = N / total_time

    results = (
        f"TEST RABBITMQ: InsultService\n"
        f"Messages: {N}\n"
        f"Total time: {total_time:.4f} seconds\n"
        f"Throughput: {throughput:.2f} msg/sec\n"
    )

    print(results)
    with open(f"results_rabbitmq_insultservice_{N}.txt", "w") as f:
        f.write(results)

if __name__ == "__main__":
    main()
