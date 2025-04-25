# Almacenar de forma centralizada variables globales y constantes
from typing import Final
from dataclasses import dataclass
from typing import Final, Dict
from queue import Queue
import uuid

@dataclass(frozen=True)
class Config:
    """Clase de configuración para almacenar variables globales y constantes."""

    # hostname
    HOSTNAME: Final[str] = "localhost"

    # server names
    NAMESERVER_NAME: Final[str] = "Pyro.NameServer"
    INSULTSTORAGE_NAME: Final[str] = "InsultStorage"
    EVENTPUBLISHER_NAME: Final[str] = "EventPublisher"
    INSULTPUBLISHER_NAME: Final[str] = "InsultPublisher"
    RAWTEXTSTORAGE_NAME: Final[str] = "RawTextStorage"
    TEXT_STORAGE_NAME: Final[str] = "TextStorage"
    CONFIG_SERVER_NAME: Final[str] = "ConfigServer"
    
    # server ports
    NAMESERVER_PORT: Final[int] = 9090
    INSULTSTORAGE_PORT: Final[int] = 4718
    EVENTPUBLISHER_PORT: Final[int] = 4719
    INSULTPUBLISHER_PORT: Final[int] = 4720
    RAWTEXTSTORAGE_PORT: Final[int] = 4721
    TEXT_STORAGE_PORT: Final[int] = 4722
    CONFIG_SERVER_PORT: Final[int] = 4723

    # server URIs
    NAMESERVER_URI: Final[str] = f"PYRO:{NAMESERVER_NAME}@{HOSTNAME}:{NAMESERVER_PORT}"
    INSULTSTORAGE_URI: Final[str] = f"PYRO:{INSULTSTORAGE_NAME}@{HOSTNAME}:{INSULTSTORAGE_PORT}"
    EVENTPUBLISHER_URI: Final[str] = f"PYRO:{EVENTPUBLISHER_NAME}@{HOSTNAME}:{EVENTPUBLISHER_PORT}"
    INSULTPUBLISHER_URI: Final[str] = f"PYRO:{INSULTPUBLISHER_NAME}@{HOSTNAME}:{INSULTPUBLISHER_PORT}"
    RAWTEXTSTORAGE_URI: Final[str] = f"PYRO:{RAWTEXTSTORAGE_NAME}@{HOSTNAME}:{RAWTEXTSTORAGE_PORT}"
    TEXT_STORAGE_URI: Final[str] = f"PYRO:{TEXT_STORAGE_NAME}@{HOSTNAME}:{TEXT_STORAGE_PORT}"
    CONFIG_SERVER_URI: Final[str] = f"PYRO:{CONFIG_SERVER_NAME}@{HOSTNAME}:{CONFIG_SERVER_PORT}"

config = Config()


class WorkerManager:
    def __init__(self):
        self.workers: Dict[str, bool] = {}
        self.client_queue: Queue = Queue()

    def add_worker(self, uri: str):
        self.workers[uri] = True

    def get_worker(self, cliente_id: str) -> str:
        for uri, state in self.workers.items():
            if state:
                self.workers[uri] = False
                print(f"Asignado {uri} a {cliente_id}")
                return uri
        self.client_queue.put(cliente_id)
        print(f"{cliente_id} en cola")
        return "In_queue"

    def free_worker(self, uri: str):
        self.workers[uri] = True
        if not self.client_queue.empty():
            cliente_id = self.client_queue.get()
            self.workers[uri] = False
            print(f"Worker {uri} asignado a {cliente_id} desde la cola")

insult_workers_manager = WorkerManager()
insult_filter_workers_manager = WorkerManager()