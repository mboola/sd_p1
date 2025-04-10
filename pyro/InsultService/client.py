from Pyro4 import Daemon, Proxy, expose, locateNS
from observer import Observer

class Client(Observer):
    @expose
    def update(self, insult):   
        print("Event: ", insult)

def main():
    with Daemon() as daemon:
        # Crear y registrar el callback
        client = Client()
        client_uri = daemon.register(client)

        # Conectarse al servidor (usa el URI que imprime tu servidor)
        server = Proxy("PYRO:InsultService@localhost:4718")

        # Añadir insulto
        result = server.add_insult("stupid")
        print("Resultado al añadir insulto:", result)

        # Suscribirse al broadcasting
        server.subscribe(client_uri)

        daemon.requestLoop()

if __name__ == "__main__":
    main()