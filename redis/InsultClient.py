import redis

# Connect to Redis
server = redis.Redis(host='localhost', port=6379, db=0, decode_responses=True)

insult_list = "insult_list"
insults = ["papanatas", "bobo", "estupido", "bobete"]

for i in range(4):
	print(f"Adding '{insults[i]}'!")
	server.rpush(insult_list, insults[i])
