import Pyro4
from Observer import Observer

class Subscriber(Observer):
    def __init__(self, uri):
        self.uri = uri

    @Pyro4.expose
    def update(self, insult):
        print(f"Event: {insult}")

    def get_uri(self):
        return self.uri
    
    def set_uri(self, uri):
        self.uri = uri

def main():
    with Pyro4.Daemon() as daemon:
        # Crear el objeto sin URI
        subscriber = Subscriber(None)

        # Registrar y obtener URI
        subscriber_uri = daemon.register(subscriber)
        subscriber.set_uri(subscriber_uri)  # Asignar URI al objeto

        # Conectarse al servidor EventPublisher
        server = Pyro4.Proxy("PYRO:EventPublisher@localhost:4719")
        server.subscribe(subscriber_uri)

        print(f"Subscriber with URI {subscriber_uri} in execution...")
        daemon.requestLoop()


if __name__ == "__main__":
    main()