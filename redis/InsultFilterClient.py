import redis
import sys

petitions = int(sys.argv[1])

# Connect to Redis
server = redis.Redis(host='localhost', port=6379, db=0, decode_responses=True)

texts_queue = "texts_queue"
raw_texts = ["Eres un papanatas!", "Tremendo bobo", "Como puedes ser tan estupido, estupido?", "bobete bobete bobo bobete"]

for i in range(petitions):
    print(f"Adding text!")
    server.rpush(texts_queue, raw_texts[i % 4])
