import redis
import re
import sys

petitions = int(sys.argv[1])

# Connect to Redis
server = redis.Redis(host='localhost', port=6379, db=0, decode_responses=True)

insult_list = "insult_list"
texts_queue = "texts_queue"
result_queue = "filtered_texts"

# Continuously listen for messages
while True:
	text = server.blpop(texts_queue, timeout = 0)
	if text:
		new_text = text[1]
		print(f"Text received: '{new_text}'")
		banned_words = server.lrange(insult_list, 0, -1)
		words = server.lrange('word_list', 0, -1)  # Get all elements
		for banned_word in banned_words:
			new_text = re.sub(banned_word, "CENSORED", new_text, flags=re.IGNORECASE)
		print(f"Text sent: '{new_text}'")
		server.rpush(result_queue, new_text)
		length = server.llen(result_queue)
		if (length >= petitions):
			server.publish("end_condition_channel", "Ended!")
