import Pyro4

# Definir la clase correctamente y exponerla
class InsultService:
    def __init__(self):
        self.insults = []         # Lista de insultos
        self.subscribers = []     # Lista de URLs de suscriptores
    
    @Pyro4.expose
    def add_insult(self, insult):
        self.insults.append(insult)
        # Notificar a cada suscriptor sobre el nuevo insulto
        for subscriber_url in self.subscribers:
            try:
                print(subscriber_url)
                proxy = Pyro4.Proxy(subscriber_url)  # Crear un proxy para el suscriptor
                proxy.notify(insult)  # Llamar al método notify del suscriptor
            except Exception as e:
                print(f"Error al notificar al suscriptor {subscriber_url}: {e}")
        return "Insulto registrado: " + insult
    
    
# Configurar el servidor
daemon = Pyro4.Daemon()  # Crear instancia del servidor
name_server = Pyro4.locateNS()  # Localizar el Name Server

# Crear una instancia de la clase correctamente
insultService = InsultService()

# Registrar el objeto en Pyro4
uri = daemon.register(insultService)
name_server.register("example.remote.object", uri)

print(f"Server with URI {uri} in execution...")
daemon.requestLoop()  # Mantener el servidor en ejecución
