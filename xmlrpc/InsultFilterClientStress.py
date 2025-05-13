import xmlrpc.client
import sys
import time

petitions = int(sys.argv[1])

# Getting server in "http://localhost:8000"
name_server = xmlrpc.client.ServerProxy('http://localhost:8000')

raw_text_storage_uri = name_server.get_raw_text_storage_node()
raw_text_storage_server = xmlrpc.client.ServerProxy(raw_text_storage_uri)

raw_texts = ["Eres un papanatas!", "Tremendo bobo", "Como puedes ser tan estupido, estupido?", "bobete bobete bobo bobete"]
n_texts = len(raw_texts)

for i in range(petitions):
    raw_text_storage_server.add_text_to_filter(raw_texts[i % n_texts])

print(f"Start time: {time.time()}", flush=True)