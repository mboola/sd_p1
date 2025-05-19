import Pyro4
import redis
import logging
import sys
from datetime import datetime, timezone

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(message)s",
    handlers=[
        logging.FileHandler("insult_filter_service.log", mode="a"),
        logging.StreamHandler()
    ]
)

@Pyro4.behavior(instance_mode="single")
class InsultFilterService:
    def __init__(self):
        self.r = redis.Redis(host='localhost', port=6379, decode_responses=True)
        self.subscribers = []

    def get_insults_list(self):
        return self.r.smembers("insults")

    def filter_text(self, text):
        insults_set = self.get_insults_list()
        words = text.split()
        censored = [
            "CENSORED" if word.lower() in insults_set else word
            for word in words
        ]
        return " ".join(censored)

    @Pyro4.expose
    def add_text(self, input_texts):
        if isinstance(input_texts, str):
            input_texts = [input_texts]

        resultados = []

        for text in input_texts:
            text = text.lower()
            filtered = self.filter_text(text)

            # Verificación más rápida usando un set
            ya_existente = self.r.sismember("filtered_texts_set", filtered)

            if not ya_existente:
                timestamp = datetime.now(timezone.utc).isoformat()
                next_id = self.r.incr("filtered_texts_id")
                self.r.hset("filtered_texts", next_id, f"{filtered}|{timestamp}")
                self.r.sadd("filtered_texts_set", filtered)  # Se guarda en el set
                logging.info(f"Texto filtrado añadido: {filtered}")
                resultados.append(f"Texto registrado: {filtered} (UTC: {timestamp})")
            else:
                logging.info(f"Texto ya registrado: {filtered}")
                resultados.append(f"Texto ya registrado: {filtered}")

        return resultados


    @Pyro4.expose
    def get_texts(self):
        raw = self.r.hgetall("filtered_texts")
        return [{ "id": k, "text": v.split("|")[0], "timestamp": v.split("|")[1] } for k, v in raw.items()]

def main():
    port = int(sys.argv[1]) # >= 50152
    name = sys.argv[2] # #InsultFilterService_{i}

    daemon = Pyro4.Daemon(port=port)
    ns = Pyro4.locateNS()
    obj = InsultFilterService()
    uri = daemon.register(obj)
    ns.register(name, uri)
    logging.info(f"{name} registrado en {uri}")
    daemon.requestLoop()

if __name__ == "__main__":
    main()
