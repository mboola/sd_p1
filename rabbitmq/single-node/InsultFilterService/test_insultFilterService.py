import time
import pika
import json
import sys
import redis

def main():
    n_is = int(sys.argv[1])
    n_if = int(sys.argv[2])
    n_pis = int(sys.argv[3])
    n_pif = int(sys.argv[4])

    credentials = pika.PlainCredentials("ar", "sar")
    parameters = pika.ConnectionParameters("localhost", credentials=credentials)
    connection = pika.BlockingConnection(parameters)
    channel = connection.channel()
    channel.queue_declare(queue="text_queue", durable=True)

    r = redis.Redis(host='localhost', decode_responses=True)
    pubsub = r.pubsub()
    pubsub.subscribe("end_condition_channel")

    print(f"📤 Sending {n_pif} texts to text_queue...")
    for i in range(n_pif):
        text = f"{i} This is a text with insult_{i}"
        message = json.dumps({"text": text})
        channel.basic_publish(
            exchange='',
            routing_key='text_queue',
            body=message,
            properties=pika.BasicProperties(delivery_mode=2)
        )
    connection.close()

    start = time.time()
    for message in pubsub.listen():
        if message['type'] == 'message':
            break
    end = time.time()

    total_time = end - start
    throughput = n_pif / total_time

    results = (
        f"TEST RABBITMQ-PUBSUB: InsultFilterService\n"
        f"Messages: {n_pif}\n"
        f"Total time: {total_time:.4f} seconds\n"
        f"Throughput: {throughput:.2f} msg/sec\n"
    )

    print(results)
    with open(f"results_rabbitmq_insultfilter_{n_is}_{n_if}_{n_pis}_{n_pif}.txt", "w") as f:
        f.write(results)

if __name__ == "__main__":
    main()