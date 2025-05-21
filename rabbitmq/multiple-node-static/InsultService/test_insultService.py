import redis
import time
import pika
import json
import sys

def main():
    n_is = int(sys.argv[1])
    n_if = int(sys.argv[2])
    n_pis = int(sys.argv[3])
    n_pif = int(sys.argv[4])

    credentials = pika.PlainCredentials("ar", "sar")
    parameters = pika.ConnectionParameters("localhost", credentials=credentials)
    connection = pika.BlockingConnection(parameters)
    channel = connection.channel()
    channel.queue_declare(queue="insult_queue", durable=True)

    r = redis.Redis(host='localhost', decode_responses=True)
    pubsub = r.pubsub()
    pubsub.subscribe("end_condition_insults")

    print(f"📤 Sending {n_pis} insults to insult_queue...")
    for i in range(n_pis):
        insult = f"insult_{i}"
        message = json.dumps({"insult": insult})
        channel.basic_publish(
            exchange='',
            routing_key='insult_queue',
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
    throughput = n_pis / total_time

    results = (
        f"TEST RABBITMQ-PUBSUB: InsultService\n"
        f"Messages: {n_pis}\n"
        f"Total time: {total_time:.4f} seconds\n"
        f"Throughput: {throughput:.2f} msg/sec\n"
    )

    print(results)
    with open(f"results_rabbitmq_pubsub_insult_{n_is}_{n_if}_{n_pis}_{n_pif}.txt", "w") as f:
        f.write(results)

if __name__ == "__main__":
    main()
