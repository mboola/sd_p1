import Pyro4
import time
import logging
import multiprocessing
import sys
import re as regex
from Observer import Observer
from Config import config

# Formato de logging:
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    datefmt='%Y-%m-%d %H:%M:%S')

class InsultFilterService(Observer):
    def __init__(self, insults, awake):
        self.insults = insults         # Lista compartida de insultos 
        self.awake = awake        

    @Pyro4.oneway
    def update(self, insult_list_updated):
        self.insults[:] = insult_list_updated
        return True

    @Pyro4.oneway
    def awake(self):
        self.awake = True
        return True
    
    @Pyro4.expose
    def ping(self):
        return True
    
def filter_texts(insults, awake, raw_storage_uri, text_storage_uri):
    """Bucle en segundo plano que filtra textos cuando awake_flag es True"""
    insult_publisher = Pyro4.Proxy(raw_storage_uri)
    text_storage_uri = Pyro4.Proxy(text_storage_uri)
    while True:
        if awake:
            if insult_publisher is None or text_storage_uri is None:
                try:
                    raw_storage = Pyro4.Proxy(raw_storage_uri)
                    text_storage = Pyro4.Proxy(text_storage_uri)
                except Pyro4.errors.CommunicationError:
                    logging.error("Error de comunicación con InsultPublisher y TextStorage, intentando intentar...")
                    continue
            
            text_to_filter = raw_storage.get_text_to_filter()
            if text_to_filter:
                logging.info(f"Texto a filtrar: {text_to_filter}")
                
                # Censura cada insulto en la lista
                for insult in insults:
                    text = regex.sub(insult, "CENSORED", text, flags=regex.IGNORECASE)
                
                logging.info(f"Texto filtrado: {text}")
                text_storage.add_text_to_filter(text)
            else:
                logging.debug("No hay texto para filtrar")
                awake.value = False #TODO Preguntar .value
        else:
            print("Esperando...")
        time.sleep(1)

def main():
    daemon = Pyro4.Daemon()
    ns = Pyro4.Proxy(config.NAMESERVER_URI)

    manager = multiprocessing.Manager()
    insults = manager.list([""])
    awake = manager.Value('b', False)

    worker_insult_filter_service = InsultFilterService(insults, awake)
    worker_insult_filter_service_uri = daemon.register(worker_insult_filter_service, objectId=config.get_id(worker_insult_filter_service))

    #Intentar registrar el worker en la lista de servicios del Config
    try:
        config.FILTER_WORKERS.append(worker_insult_filter_service_uri)
        print(f"URI registrada en Config.FILTER_WORKERS")
    except Exception as e:
        print(f"Error registrando URI en Config: {e}")
        sys.exit(1)

    raw_text_storage_uri = ns.lookup(config.RAW_TEXT_STORAGE_NAME)
    text_storage_uri = ns.lookup(config.TEXT_STORAGE_NAME)

    #TODO: Problema tengo que implementar en el Config una lista de los workers de InsultFilterService, y otros, pero que esten asociados a un puerto y id concreto

    # Proceso de filtrado en lugar de hilo
    p = multiprocessing.Process(
        target=filter_texts,
        args=(insults, awake, raw_text_storage_uri, text_storage_uri),
        daemon=True
    )

    p.start()

    #TODO: Registrar el InsultFilterService en una lista de servicios en el Config

    try:
        logging.info(f"InsultFilterService with URI: {worker_insult_filter_service_uri} in execution...")
        daemon.requestLoop()
    except KeyboardInterrupt:
        logging.info("Apagando InsultFilterService...")
        daemon.shutdown()

if __name__ == "__main__":
    main()