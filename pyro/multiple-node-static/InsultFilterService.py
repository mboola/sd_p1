import Pyro4
import time
import logging
import multiprocessing
import sys
import re as regex
from Observer import Observer
from Config import config

# TODO: Falta provar de inciar, pero no puedo hasta completar el TextStorage

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
    
def filter_texts(insults, awake, raw_uri, text_uri):
    raw_storage = Pyro4.Proxy(raw_uri)
    text_storage = Pyro4.Proxy(text_uri)
    while True:
        if awake.value:          # usa awake.value si es Value('b', …)
            try:
                text_to_filter = raw_storage.get_text_to_filter()
            except Pyro4.errors.CommunicationError:
                logging.error("Error comunicando con RawTextStorage, reintentando…")
                time.sleep(1)
                continue
            if text_to_filter:
                logging.info(f"Texto a filtrar: {text_to_filter}")
                # Asegúrate de usar una variable distinta a "text"
                filtered = text_to_filter
                for insult in insults:
                    filtered = regex.sub(insult, "CENSORED", filtered, flags=regex.IGNORECASE)
                logging.info(f"Texto filtrado: {filtered}")
                try:
                    text_storage.add_text_to_filter(filtered)
                except Pyro4.errors.CommunicationError:
                    logging.error("Error comunicando con TextStorage")
                awake.value = False
            else:
                logging.debug("No hay texto para filtrar")
        else:
            logging.debug("Esperando notificación…")
        time.sleep(1)


def main():
    daemon = Pyro4.Daemon()
    ns = Pyro4.Proxy(config.NAMESERVER_URI)

    manager = multiprocessing.Manager()
    insults = manager.list([""])
    awake = manager.Value('b', False)

    worker_insult_filter_service = InsultFilterService(insults, awake)
    worker_insult_filter_service_uri = daemon.register(worker_insult_filter_service, objectId=f"WorkerInsultFilterService_{config.get_id(worker_insult_filter_service)}")

    #Intentar registrar el worker en la lista de servicios del Config
    try:
        config.FILTER_WORKERS.append(worker_insult_filter_service_uri)
        print(f"URI registrada en Config.FILTER_WORKERS")
    except Exception as e:
        print(f"Error registrando URI en Config: {e}")
        sys.exit(1)

    raw_text_storage_uri = config.RAWTEXTSTORAGE_URI #ns.lookup(config.RAWTEXTSTORAGE_NAME)
    text_storage_uri = ns.lookup(config.TEXT_STORAGE_NAME)

    # Proceso de filtrado en lugar de hilo
    p = multiprocessing.Process(
        target=filter_texts,
        args=(insults, awake, raw_text_storage_uri, text_storage_uri),
        daemon=True
    )

    p.start()

    try:
        logging.info(f"InsultFilterService with URI: {worker_insult_filter_service_uri} in execution...")
        daemon.requestLoop()
    except KeyboardInterrupt:
        logging.info("Apagando InsultFilterService...")
        daemon.shutdown()
        #TODO: Sacar el worker de la lista de servicios del Config

if __name__ == "__main__":
    main()