import json
import re

insults = ["papanata", "soso", "burro"]

def lambda_handler(event, context):
	for record in event['Records']:
		try:
			text = json.loads(record['body']).get('text', '')
			print(f"Procesando petición con datos: {text}")

			for insult in insults:
				text = re.sub(insult, "CENSORED", text, flags=re.IGNORECASE)
			print(f"Texto filtrado: {text}")

		except Exception as e:
			print(f"Fallo rarete {e}")

	return {
		'statusCode': 200,
		'body': json.dumps('Hello from Lambda!')
	}
