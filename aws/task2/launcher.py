import boto3
import json
import time
from concurrent.futures import ThreadPoolExecutor

ACCESS_KEY = '<ACCESS_KEY>'
SECRET_KEY = '<SECRET_KEY>'
SESSION_TOKEN = '<SESSION_TOKEN>'
REGION = 'us-east-1'

sqs = boto3.client('sqs',
    region_name=REGION,
    aws_access_key_id=ACCESS_KEY,
    aws_secret_access_key=SECRET_KEY,
    aws_session_token=SESSION_TOKEN
)

# Inicialización de clientes AWS
lambda_client = boto3.client('lambda')

# ---------- FILL QUEUE ----------
def fill_queue(queue_url, num_messages=200):
    mensaje = { "text": "Lo que no hay que aguantar es a que un soso un burro y un papanata hagan estas cosas" }

    for _ in range(num_messages):
        sqs.send_message(
            QueueUrl=queue_url,
            MessageBody=json.dumps(mensaje)
        )

    print(f"{num_messages} mensajes enviados a la cola '{queue_url}'")

# ---------- INVOCACIÓN LAMBDA ----------
def invoke_lambda(lambda_name, payload):
    try:
        lambda_client.invoke(
            FunctionName=lambda_name,
            InvocationType='Event',  # asincrónica
            Payload=json.dumps(payload).encode('utf-8')
        )
        return True
    except Exception as e:
        print(f"Error invoking Lambda: {e}")
        return False

# ---------- PROCESAMIENTO DE MENSAJE ----------
def process_message(queue_url, lambda_name, message):
    payload = json.loads(message['Body'])

    if invoke_lambda(lambda_name, payload):
        sqs.delete_message(QueueUrl=queue_url, ReceiptHandle=message['ReceiptHandle'])

# ---------- AUTOESCALADOR ----------
def primitive_stream_operation(lambda_name, maxfunc, queue_url):
    while True:
        response = sqs.receive_message(
            QueueUrl=queue_url,
            MaxNumberOfMessages=min(10, maxfunc),
            WaitTimeSeconds=5
        )

        messages = response.get('Messages', [])
        if not messages:
            print("No hay mensajes.")
            time.sleep(2)
            continue

        print(f"Recibidos {len(messages)} mensajes")

        with ThreadPoolExecutor(max_workers=maxfunc) as executor:
            for message in messages:
                executor.submit(process_message, queue_url, lambda_name, message)

# ---------- MAIN ----------
if __name__ == "__main__":
    lambda_name = 'insultFilterWorker'
    queue_url = '<URL_SQS>/textFilterQueue'

    fill_queue(queue_url, num_messages=200)

    primitive_stream_operation(lambda_name, maxfunc=10, queue_url=queue_url)
