import Pyro4
from observer import Observer

class Subscriber(Observer):
    @Pyro4.expose
    def update(self, insult):   
        print("Event: ", insult)

def main():
    ns = Pyro4.locateNS()
    daemon = Pyro4.Daemon()
    notifier_server_uri = ns.lookup("Notifier")
    print("Conectando al Notifier...")
    notifier_server = Pyro4.Proxy(notifier_server_uri)
    print("Conectado al Notifier.\n")

    subscriber = Subscriber()
    subscriber_uri = daemon.register(subscriber)

    notifier_server.subscribe(subscriber_uri)
    print("Suscrito al Notifier. Esperando eventos...\n\n")

    daemon.requestLoop()

if __name__ == "__main__":
    main()