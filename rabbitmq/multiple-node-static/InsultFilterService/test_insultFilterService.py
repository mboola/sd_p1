import time
import pika
import json
import sys
import redis

def main():
    n_is = int(sys.argv[1])     # Número de InsultService
    n_if = int(sys.argv[2])     # Número de InsultFilterService
    n_pis = int(sys.argv[3])    # Número de peticiones de insultos
    n_pif = int(sys.argv[4])    # Número de textos a filtrar

    # Conexion a RabbitMQ
    credentials = pika.PlainCredentials("ar", "sar")
    parameters = pika.ConnectionParameters("localhost", credentials=credentials)
    connection = pika.BlockingConnection(parameters)
    channel = connection.channel()
    channel.queue_declare(queue="text_queue", durable=True)

    # Conexion a Redis
    r = redis.Redis(host='localhost', port=6379, decode_responses=True)

    print(f"📤 Enviando {n_pif} textos a text_queue...")

    start = time.time()
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

    # Espera hasta que Redis tenga n_pif textos procesados
    while True:
        count = r.hlen("filtered_texts")
        if count >= n_pif:
            break
        time.sleep(0.1)  # Esperar un poco antes de volver a comprobar

    end = time.time()
    total_time = end - start
    throughput = n_pif / total_time

    results = (
        f"TEST RABBITMQ: InsultFilterService (Tiempo real hasta persistencia)\n"
        f"Mensajes enviados: {n_pif}\n"
        f"Total time (envío + procesado): {total_time:.4f} segundos\n"
        f"Throughput: {throughput:.2f} mensajes/segundo\n"
    )

    print(results)
    with open(f"results_rabbitmq_insultfilterservice_{n_is}_{n_if}_{n_pis}_{n_pif}.txt", "w") as f:
        f.write(results)

if __name__ == "__main__":
    main()
