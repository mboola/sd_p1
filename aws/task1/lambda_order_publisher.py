import boto3
import csv
import io
import json
import pika
from urllib.parse import unquote
from botocore.exceptions import ClientError

# Insert here the IP of the EC2 instance
ec2_ip = '18.233.153.138'

# RabbitMQ queue names
INSULT_QUEUE = "insult_queue"
TEXT_QUEUE = "text_queue"

def lambda_handler(event, context):
	try:
		# Extract bucket and key from the S3 event and decode the key
		bucket = event['Records'][0]['s3']['bucket']['name']
		key = unquote(event['Records'][0]['s3']['object']['key'])
		print(f"Processing object: {key} from bucket: {bucket}")
		
		# Read the CSV file from S3
		s3 = boto3.client('s3')
		try:
			response = s3.get_object(Bucket=bucket, Key=key)
		except ClientError as e:
			if e.response['Error']['Code'] == "NoSuchKey":
				error_message = f"Object with key '{key}' not found in bucket '{bucket}'."
				print(error_message)
				return {
					"statusCode": 404,
					"body": error_message
				}
			else:
				raise
		
		csv_content = response['Body'].read().decode('utf-8')
		print("CSV content read from S3:")
		print(csv_content)
		
		# Parse CSV file using csv.DictReader
		csv_file = io.StringIO(csv_content)
		reader = csv.DictReader(csv_file)
		
		# Connect to RabbitMQ (replace 'PUBLIC_IP' with your RabbitMQ server's IP, and update credentials)
		credentials = pika.PlainCredentials('user', 'password123')
		connection = pika.BlockingConnection(
			pika.ConnectionParameters(
				host=ec2_ip,
				credentials=credentials
			)
		)
		channel = connection.channel()
		channel.queue_declare(queue=TEXT_QUEUE)

		print("Connected to RabbitMQ")
		
		# Process each order in the CSV and publish to RabbitMQ
		for row in reader:
			print("Processing row:", row)
			order = {
				'text': row.get('Text')
			}
			print("Processing order:", order)
			message = json.dumps(order)
			channel.basic_publish(exchange='', routing_key=TEXT_QUEUE, body=message)
			
		connection.close()
		return {
			"statusCode": 200,
			"body": "Orders published to RabbitMQ"
		}
	
	except Exception as e:
		print("Error processing order CSV: ", str(e))
		return {
			"statusCode": 500,
			"body": "Error publishing orders: " + str(e)
		}
