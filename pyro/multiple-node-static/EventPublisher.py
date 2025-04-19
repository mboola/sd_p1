import Pyro4
import random
import time
from multiprocessing import Process, Manager
from InsultStorage import InsultStorage

@Pyro4.behavior(instance_mode="single")
class EventPublisher:
    def __init__(self):
        self.insults_storage = InsultStorage().get_insults()
        self.subscribers = []  # Lista de URLs de suscriptores
    
    def get_random_insult(self):
        number_of_insults_local_list = len(self.insults_storage)
        number_of_insults_InsultStorage = InsultStorage().get_number_insults()
        
        if number_of_insults_local_list != number_of_insults_InsultStorage:
            self.insults_storage = InsultStorage().get_insults()
            #print("InsultStorage updated")
        if self.insults_storage:
            return random.choice(self.insults_storage)
        else:
            return None
        
    @Pyro4.expose
    def subscribe(self, subscriber_uri):
        if subscriber_uri not in self.subscribers:
            self.subscribers.append(subscriber_uri)
            #print("Suscriptor registrado")
            return True
        else:
            #print("Suscriptor ya registrado")
            return False

    @Pyro4.expose
    def unsubscribe(self, subscriber_uri):
        if subscriber_uri in self.subscribers:
            self.subscribers.remove(subscriber_uri)
            #print(f"Unsubscribed {subscriber_uri}")
            return True
        else:
            #print(f"Subscriber {subscriber_uri} not found")
            return False
    
    @Pyro4.expose
    def broadcast_loop(self):
        while True:
            print("⏳ Revisando...")
            if self.insults_storage and self.subscribers:
                insult = self.get_random_insult()
                for uri in self.subscribers:
                    try:
                        proxy = Pyro4.Proxy(uri)
                        # TODO: Hacer multiproceso para enviar insultos a los servicios de filtrado
                        proxy.update(insult)
                        print("📤 Enviado a:", uri)
                    except Exception as e:
                        print("❌ Error al enviar a", uri, ":", e)
            time.sleep(5)

def main():
    with Manager() as manager:
        insults = manager.list()
        subscribers = manager.list()

        obj = EventPublisher()

        # Configurar el servidor
        daemon = Pyro4.Daemon(port=4719)
        uri = daemon.register(obj, objectId="EventPublisher")

        # Iniciar proceso separado para broadcasting
        p = Process(target=obj.broadcast_loop, daemon=True)
        p.start()

        print(f"Publisher with URI {uri} in execution...")
        daemon.requestLoop()

if __name__ == "__main__":
    main()

