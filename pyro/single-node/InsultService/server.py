import Pyro4
import random
import time
from multiprocessing import Process, Manager

# Definir la clase correctamente y exponerla
@Pyro4.behavior(instance_mode="single")
class InsultService:
    def __init__(self, insults, subscribers):
        self.insults = insults         # Lista compartida de insultos
        self.subscribers = subscribers # Lista compartida de suscriptores

    @Pyro4.expose
    def add_insult(self, insult):
        if insult not in self.insults:
            self.insults.append(insult)
        else:
            return "Insulto ya registrado"
        # Notificar a cada suscriptor sobre el nuevo insulto
        for subscriber_url in self.subscribers:
            try:
                print(subscriber_url)
                proxy = Pyro4.Proxy(subscriber_url)
                proxy.update(insult)
            except Exception as e:
                print(f"Error al notificar al suscriptor {subscriber_url}: {e}")
        return "Insulto registrado: " + insult

    @Pyro4.expose
    def get_insults(self):
        return list(self.insults)

    @Pyro4.expose
    def subscribe(self, subscriber_uri):
        if subscriber_uri not in self.subscribers:
            self.subscribers.append(subscriber_uri)
            print("Suscriptor registrado")
        else:
            print("Suscriptor ya registrado")

    @Pyro4.expose
    def unsubscribe(self, subscriber_uri):
        if subscriber_uri in self.subscribers:
            self.subscribers.remove(subscriber_uri)
            print(f"Unsubscribed {subscriber_uri}")

    def get_random_insult(self):        
        return random.choice(self.insults) if self.insults else None

    def broadcast_loop(self):
        while True:
            print("⏳ Revisando...")
            if self.insults and self.subscribers:
                insult = random.choice(self.insults)
                for uri in self.subscribers:
                    try:
                        proxy = Pyro4.Proxy(uri)
                        proxy.update(insult)
                        print("📤 Enviado a:", uri)
                    except Exception as e:
                        print("❌ Error al enviar a", uri, ":", e)
            time.sleep(5)


# Ejecutar el servidor
def main():
    with Manager() as manager:
        insults = manager.list()
        subscribers = manager.list()

        obj = InsultService(insults, subscribers)

        # Configurar el servidor
        daemon = Pyro4.Daemon(port=4718)
        uri = daemon.register(obj, objectId="InsultService")

        # Iniciar proceso separado para broadcasting
        p = Process(target=obj.broadcast_loop, daemon=True)
        p.start()

        print(f"InsultService with URI {uri} in execution...")
        daemon.requestLoop()

if __name__ == "__main__":
    main()
