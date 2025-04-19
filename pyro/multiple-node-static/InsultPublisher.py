import Pyro4
import time
import multiprocessing

class InsultPublisher:
    def __init__(self):
        self.insults = []
        self.subscribers = []   # Lista de servicios de filtrado de insultos
        self.update = False     # Variable para controlar la actualización de insultos
        self.notify = False

    def update_insults(self, insult):
        self.insults.append(insult)
        self.update = True
        return True
    
    @Pyro4.expose
    def subscribe(self, subscriber_uri):
        if subscriber_uri not in self.subscribers:
            self.subscribers.append(subscriber_uri)
            return True
        else:
            return False
    
    @Pyro4.expose
    def unsubscribe(self, subscriber_uri):
        if subscriber_uri in self.subscribers:
            self.subscribers.remove(subscriber_uri)
            return True
        else:
            return False
     
    def send_insults_to_filter(self, insult_filter_service, insults):
        try:
            proxy = Pyro4.Proxy(insult_filter_service)
            proxy.update(insults)
            print("📤 Enviado a:", insult_filter_service)
        except Exception as e:
            print("❌ Error al enviar a", insult_filter_service, ":", e)

    @Pyro4.expose
    def broadcast_updates(self):
        while True:
            if self.update:
                jobs = []
                for subscriber in self.subscribers:
                    p = multiprocessing.Process(
                        target=self.send_insults_to_filter,
                        args=(subscriber, self.insults.copy())
                    )
                    p.start()
                    jobs.append(p)
                for job in jobs:
                    job.join()
                self.update = False
            time.sleep(5)

    @Pyro4.expose
    def notify_filter_services(self):
        while True:
            if self.notify or self.update:
                for subscriber in self.subscribers:
                    try:
                        proxy = Pyro4.Proxy(subscriber)
                        if self.update:
                            proxy.update(self.insults.copy())
                        if self.notify:
                            proxy.awake()
                        print("📤 Enviado a:", subscriber)
                    except Exception as e:
                        print("❌ Error al enviar a", subscriber, ":", e)
                self.notify = False
                self.update = False
            time.sleep(5)

def main():
    publisher = InsultPublisher()
    daemon = Pyro4.Daemon(port=4720)
    uri = daemon.register(publisher, objectId="InsultPublisher")

    p = multiprocessing.Process(target=publisher.broadcast_updates, daemon=True)
    p.start()

    print(f"InsultPublisher with URI {uri} in execution...")
    daemon.requestLoop()

if __name__ == "__main__":
    main()
        