import logging
import Pyro4
from Config import config

# Formato de logging:
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    datefmt='%Y-%m-%d %H:%M:%S')

class TextStorage:
    def __init__(self, insults):
        self.censored_text = []

    @Pyro4.oneway
    def add_censored_text(self, text):
        self.censored_text.append(text)
        logging.info(f"Texto censurado añadido: {text}")
        return True
    
    @Pyro4.expose
    def get_censored_texts(self):
        """Devuelve la lista completa de textos censurados"""
        return list(self.censored_text)
    
    @Pyro4.expose
    def ping(self):
        """Método de prueba para verificar la conexión"""
        return True
    
def main():
    daemon = Pyro4.Daemon(port=config.TEXT_STORAGE_PORT)
    ns = Pyro4.Proxy(config.NAMESERVER_URI)
    
    # Registrar el servicio de almacenamiento de textos censurados
    text_storage = TextStorage([])
    text_storage_uri = daemon.register(text_storage, objectId=config.TEXT_STORAGE_NAME)
    ns.register(config.TEXT_STORAGE_NAME, text_storage_uri)
    
    try:
        logging.info(f"{config.TEXT_STORAGE_NAME} con URI: {text_storage_uri} en ejecución...")
        daemon.requestLoop()
    except KeyboardInterrupt:
        logging.info("Apagando CensoredTextStorage...")
        daemon.shutdown()

if __name__ == "__main__":
    main()