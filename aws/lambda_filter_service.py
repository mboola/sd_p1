import json
import re
import pika

EC2_IP = '18.233.153.138'
TEXT_QUEUE = "text_queue"
RESULT_QUEUE = "result_queue"

insults = [
	"papanatas", "bobo", "estupido", "bobete",   "nincompoop", "buffoon", "dimwit", "clod", "doofus", "numbskull", "dullard", "simpleton", "twit", "loon",
	"blockhead", "nitwit", "goofball", "bonehead", "blunderer", "muttonhead", "dunderhead", "chowderhead", "fool",
	"airhead", "birdbrain", "dunce", "lunkhead", "meathead", "dingbat", "twaddle", "clown", "bumbler", "nit",
	"lamebrain", "moron", "peabrain", "wazzock", "drongo", "spanner", "mug", "goblin", "wally", "twerp",
	"prat", "numpty", "dope", "tool", "oaf", "muppet", "bozo", "git", "pillock", "klutz",
	"turkey", "nerfherder", "twonk", "schmuck", "pipsqueak", "grump", "rascal", "scallywag", "scamp", "wretch",
	"rapscallion", "cad", "blaggard", "charlatan", "twaddlehead", "snollygoster", "blowhard", "loudmouth", "scoundrel", "knave",
	"toerag", "scuzzball", "nutter", "dingus", "ninny", "crank", "cur", "yokel", "rube", "goon",
	"hooligan", "lackwit", "dodo", "ignoramus", "zany", "bungler", "gomer", "slugabed", "leech", "drip",
	"flake", "loonball", "doink", "snob", "weasel", "cringer", "poser", "cheeser", "slug", "grouch"
]

def create_connection():
	credentials = pika.PlainCredentials('user', 'password123')
	return pika.BlockingConnection(
		pika.ConnectionParameters(
			host=EC2_IP,
			credentials=credentials
		)
	)

# Process 50 petitions. If for some reason we obtain a message
# from the queue and it is empty it means there are no more msg
# and we end this lambda execution
def lambda_handler(event, context):

	connection = create_connection()
	channel = connection.channel()

	print("Lambda executed!!")

	for i in range(50):
		print(i)
		method_frame, header_frame, body = channel.basic_get(queue=TEXT_QUEUE, auto_ack=False)
		if method_frame:
			#Process msg
			body = body.decode('utf-8')
			order = json.loads(body)
			text = order.get('text')

			for insult in insults:
				text = re.sub(insult, "CENSORED", text, flags=re.IGNORECASE)

			print(text)

			channel.basic_ack(method_frame.delivery_tag)
		else:
			print("No text to filter!!!!")
			break

	connection.close()

	print("Lambda ended!!")

	return {
		'statusCode': 200,
		'body': json.dumps('Ended')
	}
