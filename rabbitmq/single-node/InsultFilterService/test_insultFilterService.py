import time
import pika
import json
import sys

def main():
    n_is = int(sys.argv[1])     # Numero de InsultService
    n_if = int(sys.argv[2])     # Numero de InsultFilterService
    n_pis = int(sys.argv[3])    # Numero de peticiones de insultos
    n_pif = int(sys.argv[4])    # Numero de peticiones de textos


    credentials = pika.PlainCredentials("ar", "sar")
    parameters = pika.ConnectionParameters("localhost", credentials=credentials)
    connection = pika.BlockingConnection(parameters)
    channel = connection.channel()
    channel.queue_declare(queue="text_queue", durable=True)

    print(f"📤 Sending {n_pif} texts to text_queue...")

    start = time.time()
    for i in range(n_pif):
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
    throughput = n_pif / total_time

    results = (
        f"TEST RABBITMQ: InsultFilterService\n"
        f"Messages: {n_pif}\n"
        f"Total time: {total_time:.4f} seconds\n"
        f"Throughput: {throughput:.2f} msg/sec\n"
    )

    print(results)
    with open(f"results_rabbitmq_insultfilterservice_{n_is}_{n_if}_{n_pis}_{n_pif}.txt", "w") as f:
        f.write(results)

if __name__ == "__main__":
    main()
