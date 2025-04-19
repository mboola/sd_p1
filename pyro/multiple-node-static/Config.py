# Almacenar de forma centralizada variables globales y constantes
from typing import Final
from dataclasses import dataclass
from typing import Final, ClassVar, Union, List

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
    
    # server ports
    NAMESERVER_PORT: Final[int] = 9090
    INSULTSTORAGE_PORT: Final[int] = 4718
    EVENTPUBLISHER_PORT: Final[int] = 4719
    INSULTPUBLISHER_PORT: Final[int] = 4720
    RAWTEXTSTORAGE_PORT: Final[int] = 4721
    TEXT_STORAGE_PORT: Final[int] = 4722

    # server URIs
    NAMESERVER_URI: Final[str] = f"PYRONAME:{NAMESERVER_NAME}@{HOSTNAME}:{NAMESERVER_PORT}"
    INSULTSTORAGE_URI: Final[str] = f"PYRONAME:{INSULTSTORAGE_NAME}@{HOSTNAME}:{INSULTSTORAGE_PORT}"
    EVENTPUBLISHER_URI: Final[str] = f"PYRONAME:{EVENTPUBLISHER_NAME}@{HOSTNAME}:{EVENTPUBLISHER_PORT}"
    INSULTPUBLISHER_URI: Final[str] = f"PYRONAME:{INSULTPUBLISHER_NAME}@{HOSTNAME}:{INSULTPUBLISHER_PORT}"
    RAWTEXTSTORAGE_URI: Final[str] = f"PYRONAME:{RAWTEXTSTORAGE_NAME}@{HOSTNAME}:{RAWTEXTSTORAGE_PORT}"
    TEXT_STORAGE_URI: Final[str] = f"PYRONAME:{TEXT_STORAGE_NAME}@{HOSTNAME}:{TEXT_STORAGE_PORT}"

    # lista de URIs de filtros de insultos registrados
    FILTER_WORKERS: ClassVar[List[str]] = []
    INSULT_WORKERS: ClassVar[List[str]] = []
    
    # autoincrement id workers:
    worker_insult_filter_service_id: int = 0

    @classmethod
    # Ejemplo con id(obj)
    def get_id(cls, obj):
        return str(id(obj))


config = Config()