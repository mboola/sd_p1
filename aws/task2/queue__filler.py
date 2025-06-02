import boto3
import json

petitions = 60
ACCESS_KEY = "<ACCESS_KEY>"
SECRET_KEY = "<SECRET_KEY>"
SESSION_TOKEN = "<SESSION_TOKEN>"

queue_url = "<queue_url>"
message = "Lo que no hay que aguantar es que un soso un burro y un papanatas hagan estas cosas"

sqs = boto3.client(
        'sqs',
        region_name='us-east-1',
        aws_access_key_id=ACCESS_KEY,
        aws_secret_access_key=SECRET_KEY,
        aws_session_token=SESSION_TOKEN
)

def fill_queue(num_messages):
        text = {"text": message}
        for _ in range(num_messages):
                sqs.send_message(
                        QueueUrl=queue_url,
                        MessageBody=json.dumps(text)
                )

fill_queue(petitions)