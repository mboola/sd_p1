import redis
import time

# Connect to Redis
server = redis.Redis(host='localhost', port=6379, db=0, decode_responses=True)

# While
pubsub = server.pubsub()
pubsub.subscribe("end_condition_channel")

# Start timing
start_time = time.time()

for message in pubsub.listen():
	if message['type'] == 'message':
		break

# Done
print(f"Total time: {time.time() - start_time:.2f} seconds")
