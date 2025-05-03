import Pyro4
import redis
import sys
import logging

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(message)s",
    handlers=[
        logging.FileHandler("insult_service.log", mode="a"),
        logging.StreamHandler()
    ]
)

@Pyro4.behavior(instance_mode="single")
class InsultService:
    def __init__(self):
        self.r = redis.Redis(host='localhost', port=6379, decode_responses=True)

    @Pyro4.expose
    def add_insult(self, insult_or_list):
        if isinstance(insult_or_list, str):
            insult_or_list = [insult_or_list]

        resultados = []
        for insult in insult_or_list:
            insult = insult.lower()
            if not self.r.sismember("insults", insult):
                self.r.sadd("insults", insult)
                logging.info(f"Insulto añadido: {insult}")
                resultados.append(f"Insulto registrado: {insult}")
            else:
                logging.info(f"Insulto ya registrado: {insult}")
                resultados.append(f"Insulto ya registrado: {insult}")
        return resultados

    @Pyro4.expose
    def get_insults(self):
        return list(self.r.smembers("insults"))

def main():
    port = int(sys.argv[1]) # >= 49152
    name = sys.argv[2] #InsultService_{i}

    daemon = Pyro4.Daemon(port=port)
    ns = Pyro4.locateNS()
    obj = InsultService()
    uri = daemon.register(obj)
    ns.register(name, uri)
    logging.info(f"{name} registrado en {uri}")
    daemon.requestLoop()

if __name__ == "__main__":
    main()
