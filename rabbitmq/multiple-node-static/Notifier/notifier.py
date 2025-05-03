import Pyro4
import redis
import time
import random
import logging
from multiprocessing import Process, Manager

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(message)s"
)

@Pyro4.behavior(instance_mode="single")
class Notifier:
    def __init__(self, subscribers):
        self.r = redis.Redis(host='localhost', port=6379, decode_responses=True)
        self.subscribers = subscribers  # ← lista compartida

    @Pyro4.expose
    def subscribe(self, subscriber_uri):
        if subscriber_uri not in self.subscribers:
            self.subscribers.append(subscriber_uri)
            logging.info(f" Suscriptor añadido: {subscriber_uri}")
        else:
            logging.info("Suscriptor ya existente")

    @Pyro4.expose
    def unsubscribe(self, subscriber_uri):
        if subscriber_uri in self.subscribers:
            self.subscribers.remove(subscriber_uri)
            logging.info(f" Suscriptor eliminado: {subscriber_uri}")

def broadcast_loop(subscribers):
    r = redis.Redis(host='localhost', port=6379, decode_responses=True)
    while True:
        insults = list(r.smembers("insults"))
        if not insults:
            logging.info(" No hay insultos disponibles.")
        elif not subscribers:
            logging.info(" No hay suscriptores registrados.")
        else:
            insult = random.choice(insults)
            for uri in list(subscribers):  # usar copia por seguridad
                try:
                    proxy = Pyro4.Proxy(uri)
                    proxy.update(insult)
                    logging.info(f" Enviado a: {uri}")
                except Exception as e:
                    logging.warning(f" Error al enviar a {uri}: {e}")
        time.sleep(5)

def main():
    with Manager() as manager:
        subscribers = manager.list()

        obj = Notifier(subscribers)
        daemon = Pyro4.Daemon(port=4719)
        ns = Pyro4.locateNS()
        uri = daemon.register(obj, objectId="Notifier")
        ns.register("Notifier", uri)
        logging.info(f"Notifier registrado en {uri}")

        p = Process(target=broadcast_loop, args=(subscribers,), daemon=True)
        p.start()

        daemon.requestLoop()

if __name__ == "__main__":
    main()
