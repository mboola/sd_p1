# I suppose this is used to check messages

import redis

r = redis.Redis(host='localhost', port=6379, decode_responses=True)

print("\n CONTADOR 'filtered_texts_id':")
print(r.get("filtered_texts_id"))

print("INSULTOS (SET):")
insults = r.smembers("insults")
for i, insult in enumerate(sorted(insults), 1):
    print(f"{i}. {insult}")

print("\nTEXTOS FILTRADOS (HASH):")
textos = r.hgetall("filtered_texts")
for key in sorted(textos, key=int):
    texto, timestamp = textos[key].split("|")
    print(f"{key}. {texto}  (UTC: {timestamp})")
