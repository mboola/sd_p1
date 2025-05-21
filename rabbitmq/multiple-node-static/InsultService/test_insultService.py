import time
import pika
import json
import sys
import redis

def main():
    n_is = int(sys.argv[1])     # Número de InsultService
    n_if = int(sys.argv[2])     # Número de InsultFilterService
    n_pis = int(sys.argv[3])    # Número de peticiones de insultos
    n_pif = int(sys.argv[4])    # Número de peticiones de textos

    # Conexión a RabbitMQ
    credentials = pika.PlainCredentials("ar", "sar")
    parameters = pika.ConnectionParameters("localhost", credentials=credentials)
    connection = pika.BlockingConnection(parameters)
    channel = connection.channel()
    channel.queue_declare(queue="insult_queue", durable=True)

    # Conexión a Redis
    r = redis.Redis(host='localhost', port=6379, decode_responses=True)

    print(f"📤 Enviando {n_pis} insultos a insult_queue...")

    start = time.time()
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

    # Esperar hasta que Redis registre todos los insultos
    while True:
        count = r.scard("insults")
        if count >= n_pis:
            break
        time.sleep(0.1)

    end = time.time()
    total_time = end - start
    throughput = n_pis / total_time

    results = (
        f"TEST RABBITMQ: InsultService (Tiempo real hasta persistencia)\n"
        f"Mensajes enviados: {n_pis}\n"
        f"Total time (envío + procesado): {total_time:.4f} segundos\n"
        f"Throughput: {throughput:.2f} mensajes/segundo\n"
    )

    print(results)
    with open(f"results_rabbitmq_insultservice_{n_is}_{n_if}_{n_pis}_{n_pif}.txt", "w") as f:
        f.write(results)

if __name__ == "__main__":
    main()
