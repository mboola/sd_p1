# 2
import Pyro4
import multiprocessing
import time

@Pyro4.behavior(instance_mode="single")
class InsultStorage:
    def __init__(self):
        self.insults = []
        self.new_insults = []  # Lista de insultos recibidos

    @Pyro4.expose
    def update_insults(self, insult):
        #Iterar sobre la lista de insultos y si no lo encuentra lo añade:
        #Si el insulto no está en la lista de insultos, lo añadimos
        #Si el insulto ya está en la lista, no hacemos nada
        for actual_insult in self.insults:
            if actual_insult not in self.insults:
                if insult not in self.new_insults:
                    self.new_insults.append(actual_insult)
        new_list = self.insults
        new_list.append(self.new_insults)
        
        return new_list
        
    @Pyro4.expose
    def get_insults(self):
        new_list = self.insults
        new_list.append(self.new_insults)
        return new_list
    
    @Pyro4.expose
    def get_number_insults(self):
        return len(self.insults)
    
def background_updater(insults, new_insults):
    while True:
        if new_insults:
            for insult in list(new_insults):
                if insult not in insults:
                    insults.append(insult)
            new_insults[:] = []
        time.sleep(5)

def main():
    manager = multiprocessing.Manager()
    insults = manager.list()
    new_insults = manager.list()

    ns = Pyro4.locateNS()
    config_server_uri = ns.lookup("ConfigServer")    
    config_server = Pyro4.Proxy(config_server_uri)

    insult_storage_name = config_server.get_insultstorage_name()
    insult_storage_port = config_server.get_insultstorage_port()

    # Crear el proceso del actualizador
    updater_process = multiprocessing.Process(target=background_updater, args=(insults, new_insults))
    updater_process.daemon = True
    updater_process.start()

    daemon = Pyro4.Daemon(port=insult_storage_port)
    insult_storage = InsultStorage()
    insult_storage_uri = daemon.register(insult_storage, objectId=insult_storage_name)
    ns.register(insult_storage_name, insult_storage_uri)
    print(f"InsultStorage with URI: {insult_storage_uri} in execution...")
    daemon.requestLoop()

if __name__ == "__main__":
    main()