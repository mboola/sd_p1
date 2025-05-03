# Almacenar de forma centralizada variables globales y constantes
import random
from typing import Final
from dataclasses import dataclass
from typing import Final

@dataclass(frozen=True)
class Config:
    """Clase de configuración para almacenar variables globales y constantes."""

    # hostname
    HOSTNAME: Final[str] = "localhost"

    # server names
    NAMESERVER_NAME: Final[str] = "Pyro.NameServer"
    INSULTPUBLISHER_NAME: Final[str] = "InsultPublisher"
    
    # server ports
    NAMESERVER_PORT: Final[int] = 9090
    INSULTPUBLISHER_PORT: Final[int] = 4720

    # server URIs
    NAMESERVER_URI: Final[str] = f"PYRO:{NAMESERVER_NAME}@{HOSTNAME}:{NAMESERVER_PORT}"
    INSULTPUBLISHER_URI: Final[str] = f"PYRO:{INSULTPUBLISHER_NAME}@{HOSTNAME}:{INSULTPUBLISHER_PORT}"

config = Config()