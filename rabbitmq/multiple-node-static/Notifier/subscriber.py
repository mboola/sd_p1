import pika
import json

def main():
    credentials = pika.PlainCredentials("ar", "sar")
    parameters = pika.ConnectionParameters("localhost", credentials=credentials)
    connection = pika.BlockingConnection(parameters)
    channel = connection.channel()

    channel.exchange_declare(exchange="insult_broadcast", exchange_type="fanout")
    result = channel.queue_declare(queue="", exclusive=True)
    queue_name = result.method.queue

    channel.queue_bind(exchange="insult_broadcast", queue=queue_name)

    print("[READY] Waiting for broadcast insults...")

    def callback(ch, method, properties, body):
        message = json.loads(body)
        insult = message.get("insult", "[unknown]")
        print("Event: ", insult)

    channel.basic_consume(queue=queue_name, on_message_callback=callback, auto_ack=True)
    channel.start_consuming()

if __name__ == "__main__":
    main()