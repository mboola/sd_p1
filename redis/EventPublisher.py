import redis
import time
import random

# Connect to Redis
server = redis.Redis(host='localhost', port=6379, db=0, decode_responses=True)
insult_list = "insult_list"
channel_name = "event_channel"

while True:
	n_insults = server.llen(insult_list)
	if n_insults != 0:
		index = random.randint(0, n_insults - 1)
		random_insult = server.lindex(insult_list, index)
	
		# Notify subscribers
		server.publish("event_channel", random_insult)
		print(f"Insult broadcasted: {random_insult}")
	time.sleep(5)
