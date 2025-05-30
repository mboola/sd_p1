import json

def lambda_handler(event, context):
    print("Evento recibido:", json.dumps(event))
    insults = ["papanata", "soso", "burro"]

    # Asume que usas SQS trigger
    for record in event.get("Records", []):
        body = record["body"]
        data = json.loads(body)
        text = data.get('text', '')

        for insult in insults:
            text = text.replace(insult, "CENSORED")

        print(f"Texto filtrado: {text}")

    return {
        'statusCode': 200,
        'body': json.dumps({'message': 'Procesado'})
    }
