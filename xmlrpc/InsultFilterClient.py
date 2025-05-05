import xmlrpc.client
import time

# Getting server in "http://localhost:8000"
name_server = xmlrpc.client.ServerProxy('http://localhost:8000')

raw_text_storage_uri = name_server.get_raw_text_storage_node()

raw_texts = ["Eres un papanatas!", "Tremendo bobo", "Como puedes ser tan estupido, estupido?", "bobete bobete bobo bobete"]

i = 0
raw_text_storage_server = xmlrpc.client.ServerProxy(raw_text_storage_uri)
for i in range(100):
    #print(f"Adding text!")
    raw_text_storage_server.add_text_to_filter(raw_texts[i % 4])
