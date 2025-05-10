import pika
import json
import sys
import time

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

n_insults = len(insults)

petitions = int(sys.argv[1])

#credentials = pika.PlainCredentials("ar", "sar")
parameters = pika.ConnectionParameters("localhost")
connection = pika.BlockingConnection(parameters)
channel = connection.channel()

channel.queue_declare(queue="insult_queue", durable=True)

def send_insult(i, channel):
	try:
		message = json.dumps({"insult": insults[i % n_insults]})
		channel.basic_publish (
			exchange='',
			routing_key='insult_queue',
			body=message,
			properties=pika.BasicProperties(delivery_mode=2)
		)
		return "sent"
	except Exception as e:
		print(f"Error: {e}")
		return "wtf"

# Start timing
start_time = time.time()

for i in range(petitions):
	send_insult(i, channel)

# Done
print(f"Total time: {time.time() - start_time:.2f} seconds")

connection.close()
