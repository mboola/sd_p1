import xmlrpc.client
import time

# Getting server in "http://localhost:8000"
name_server = xmlrpc.client.ServerProxy('http://localhost:8000')

raw_text_storage_uri = name_server.get_raw_text_storage_node()

raw_texts = ["Eres un papanatas!", "Tremendo bobo", "Como puedes ser tan estupido, estupido?", "bobete bobete bobo bobete"]

i = 0
for i in range(3):
    print(f"Adding '{raw_texts[i]}' to Raw Text Storage URI '{raw_text_storage_uri}'!")
    raw_text_storage_server = xmlrpc.client.ServerProxy(raw_text_storage_uri)
    raw_text_storage_server.add_text_to_filter(raw_texts[i])
    time.sleep(1)
