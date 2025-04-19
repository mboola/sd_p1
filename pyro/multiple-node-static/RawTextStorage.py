import Pyro4
import queue
import logging
import time
import multiprocessing
from Config import config

# Formato de logging:
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    datefmt='%Y-%m-%d %H:%M:%S')

class RawTextStorage:
    def __init__(self, shared_state):
        self.shared_state = shared_state
    
    @Pyro4.oneway # decorator to mark a method to be oneway (client won't wait for a response)
    def add_text_to_filter(self, text):
        self.shared_state.text_to_censor.put(text)
        self.shared_state.petitions = True
        return True
    
    @Pyro4.expose
    def get_text_to_filter(self):
        try:
            text = self.shared_state.text_to_censor.get(timeout=1)
            logging.info(f"Obtenido texto: {text}")
            return text
        except queue.Empty:
            logging.debug("No hay texto para filtrar")
            return ""
        
    @Pyro4.expose
    def ping(self):
        return True
    
def notify_petitions(insult_publisher_uri, shared_state): #TODO
    insult_publisher = Pyro4.Proxy(insult_publisher_uri)

    while True:
        time.sleep(5)
        if shared_state.petitions:
            if insult_publisher is None:
                try:
                    insult_publisher = Pyro4.Proxy(insult_publisher_uri)
                except Pyro4.errors.CommunicationError:
                    logging.error("Error de comunicación con InsultPublisher, intentando intentar...")
                    time.sleep(5)
                    continue

            logging.info("Hay peticiones de texto para filtrar")
            insult_publisher.notify_filter_services() #TODO: Implementar el método notify_filter_services en InsultPublisher
            # Reset petitions a False  after processing
            shared_state.petitions = False
        else:
            logging.debug("No hay peticiones de texto para filtrar")
        time.sleep(5)


def main():
    # Arranca daemon y Name Server
    daemon = Pyro4.Daemon(port=4721)
    insult_publisher_uri = config.INSULTPUBLISHER_URI
    
    # Manager para compartir estado entre procesos
    manager = multiprocessing.Manager()
    shared_state = manager.Namespace()
    
    shared_state.text_to_censor = manager.Queue()
    shared_state.petitions = False

    raw_text_storage = RawTextStorage(shared_state)
    uri = daemon.register(raw_text_storage, objectId="RawTextStorage")

    p = multiprocessing.Process(target=notify_petitions,
                        args=(insult_publisher_uri, shared_state),
                        daemon=True)
    p.start()

    try:
        logging.info(f"RawTextStorage with URI: {uri} in execution...")
        daemon.requestLoop()
    except KeyboardInterrupt:
        logging.info("Apagando nodo RawTextStorage...")
        daemon.shutdown()


if __name__ == "__main__":
    main()