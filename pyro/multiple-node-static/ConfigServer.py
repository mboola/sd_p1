import Pyro4
from Config import config, insult_workers_manager, insult_filter_workers_manager

@Pyro4.expose
class ConfigServer:
    def __init__(self):
        self.config = config
        self.insult_workers = insult_workers_manager
        self.insult_filter_workers = insult_filter_workers_manager

    def get_insult_worker(self, client_id):
        return self.insult_workers.get_worker(client_id)

    def free_insult_worker(self, uri):
        self.insult_workers.free_worker(uri)

    def get_insult_filter_worker(self, client_id):
        return self.insult_filter_workers.get_worker(client_id)

    def free_insult_filter_worker(self, uri):
        self.insult_filter_workers.free_worker(uri)
    
    #Get names:
    def get_hostname(self):
        return self.config.HOSTNAME
    
    def get_nameserver_name(self):
        return self.config.NAMESERVER_NAME
    
    def get_insultstorage_name(self):
        return self.config.INSULTSTORAGE_NAME
    
    def get_eventpublisher_name(self):
        return self.config.EVENTPUBLISHER_NAME
    
    def get_insultpublisher_name(self):
        return self.config.INSULTPUBLISHER_NAME
    
    def get_rawtextstorage_name(self):
        return self.config.RAWTEXTSTORAGE_NAME
    
    def get_textstorage_name(self):
        return self.config.TEXT_STORAGE_NAME
    
    def get_config_server_name(self):
        return self.config.CONFIG_SERVER_NAME
    
    # Get ports:
    def get_nameserver_port(self):
        return self.config.NAMESERVER_PORT
    
    def get_insultstorage_port(self):
        return self.config.INSULTSTORAGE_PORT
    
    def get_eventpublisher_port(self):  
        return self.config.EVENTPUBLISHER_PORT
    
    def get_insultpublisher_port(self):
        return self.config.INSULTPUBLISHER_PORT
    
    def get_rawtextstorage_port(self):
        return self.config.RAWTEXTSTORAGE_PORT
    
    def get_textstorage_port(self):
        return self.config.TEXT_STORAGE_PORT
    
    def get_config_server_port(self):
        return self.config.CONFIG_SERVER_PORT
    
    # Get URIs:
    def get_nameserver_uri(self):
        return self.config.NAMESERVER_URI 
    
    def get_insultstorage_uri(self):
        return self.config.INSULTSTORAGE_URI
    
    def get_eventpublisher_uri(self):
        return self.config.EVENTPUBLISHER_URI
    
    def get_insultpublisher_uri(self):
        return self.config.INSULTPUBLISHER_URI
    
    def get_rawtextstorage_uri(self):
        return self.config.RAWTEXTSTORAGE_URI
    
    def get_textstorage_uri(self):
        return self.config.TEXT_STORAGE_URI
    
    def get_config_server_uri(self):
        return self.config.CONFIG_SERVER_URI

if __name__ == "__main__":
    
    daemon = Pyro4.Daemon(host=config.HOSTNAME, port=config.CONFIG_SERVER_PORT)
    ns = Pyro4.locateNS(host=config.HOSTNAME, port=config.NAMESERVER_PORT)
    config_server_uri = daemon.register(ConfigServer())
    ns.register(config.CONFIG_SERVER_NAME, config_server_uri)
    print(f"Servidor corriendo. URI: {config_server_uri}")
    daemon.requestLoop()
