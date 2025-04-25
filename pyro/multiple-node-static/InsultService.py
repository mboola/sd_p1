# 
import Pyro4
import logging
import time
import sys
import multiprocessing
import copy

# Formato de logging:
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    datefmt='%Y-%m-%d %H:%M:%S')

class InsultService:
    def __init__(self, new_insults, last_updated_insults):
        # Listas compartidas mediante Manager
        self.new_insults = new_insults
        self.last_updated_insults = last_updated_insults

    @Pyro4.oneway
    def add_insult(self, insult):
        """Añade un insulto pendiente para actualizar"""
        if insult not in self.last_updated_insults and insult not in self.new_insults:
            self.new_insults.append(insult)
            logging.info(f"Added insult '{insult}' to new_insults")
        else:
            return False
        return True
    
    @Pyro4.expose
    def ping(self):
        return "pong"
    
def update_insults_loop(new_insults, last_updated_insults, insult_storage_uri):
    insult_storage = Pyro4.Proxy(insult_storage_uri)
    while True:
        try:
            # Copia profunda y filtrado de listas vacías
            filtered = [copy.deepcopy(ins) for ins in list(new_insults) if not (isinstance(ins, list) and len(ins) == 0)]

            if filtered:
                updated = insult_storage.update_insults(filtered)
                logging.info(f"Fetched updated insults: {updated}")

                # Mover nuevos a last_updated_insults
                last_updated_insults.extend(filtered)
                logging.info(f"Moved {filtered} to last_updated_insults")
                new_insults[:] = []

                # Añadir faltantes del storage a last_updated_insults
                for ins in updated:
                    if ins not in last_updated_insults:
                        last_updated_insults.append(ins)
                        logging.info(f"Added insult '{ins}' from storage to last_updated_insults")

        except Pyro4.errors.CommunicationError:
            logging.error("Error comunicando con InsultStorage, reintentando...")

        time.sleep(3)

def main():
    # Manager para listas compartidas
    manager = multiprocessing.Manager()
    
    new_insults = manager.list()
    last_updated_insults = manager.list()

    # Crea daemon y proxy al Name Server
    daemon = Pyro4.Daemon()
    ns = Pyro4.locateNS()
    config_server_uri = ns.lookup("ConfigServer")    
    config_server = Pyro4.Proxy(config_server_uri)

    # Instancia el servicio con referencias a listas compartidas
    insult_service = InsultService(new_insults, last_updated_insults)
    object_id = f"InsultService_{config_server.get_id()}"
    insult_service_uri = daemon.register(insult_service, objectId=object_id)
    ns.register(object_id, insult_service_uri)
    insult_storage_uri = ns.lookup(config_server.get_insultstorage_name())
    logging.info(f"InsultService disponible en {insult_service_uri}")
    
    #Intentar registrar el worker en la lista de servicios del Config
    try:
        config_server.add_insult_worker(insult_service_uri)
        logging.info(f"URI registrada en Config.INSULT_WORKERS")
    except Exception as e:
        print(f"Error registrando URI en Config: {e}")
        sys.exit(1)
    
    # Inicia proceso de sincronización en segundo plano
    p = multiprocessing.Process(
        target=update_insults_loop,
        args=(new_insults, last_updated_insults, insult_storage_uri),
        daemon=True
    )
    p.start()

    # Ejecuta el bucle de servicio
    try:
        logging.info(f"InsultService with URI: {insult_service_uri} in execution...")
        daemon.requestLoop()
    except KeyboardInterrupt:
        logging.info("Apagando InsultService...")
        daemon.shutdown()
        config_server.free_insult_worker(insult_service_uri)
        logging.info(f"URI {insult_service_uri} liberada de Config.INSULT_WORKERS")

if __name__ == "__main__":
    main()