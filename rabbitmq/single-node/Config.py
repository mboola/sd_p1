# Almacenar de forma centralizada los nombres de las variables globales y constantes, y puertos fijos
from typing import Final
from dataclasses import dataclass
from typing import Final

@dataclass(frozen=True)
class Config:
    """Clase de configuración para almacenar variables globales y constantes."""

    # hostname
    HOSTNAME: Final[str] = "localhost"

    # server names
    NAMESERVER_NAME: Final[str] = "NameServer"
    NOTIFIER_NAME: Final[str] = "Notifier"
    
    # server ports
    NAMESERVER_PORT: Final[int] = 9090
    NOTIFIER_PORT: Final[int] = 4719

    # server URIs
    NAMESERVER_URI: Final[str] = f"PYRO:{NAMESERVER_NAME}@{HOSTNAME}:{NAMESERVER_PORT}"
    INSULTPUBLISHER_URI: Final[str] = f"PYRO:{NOTIFIER_NAME}@{HOSTNAME}:{NOTIFIER_PORT}"

    # rabbitmq username and passwords
    USERNAME: Final[str] = "ar"
    PASSWORD: Final[str] = "sar"
    RABBITMQ_HOST: Final[str] = "localhost"

    # rabbitmq queue name
    INSULTFILTERSERVICE_QUEUE_NAME: Final[str] = "text_queue"
    INSULTSERVICE_QUEUE_NAME: Final[str] = "insult_queue"

    # rabbitmq ports
    RABBITMQ_PORT: Final[int] = 5672
    INSULTFILTERSERVICE_PORT_INIT: Final[int] = 50152
    INSULTSERVICE_PORT_INIT: Final[int] = 49152

    # redis server
    REDIS_HOST: Final[str] = "localhost"
    REDIS_PORT: Final[int] = 6379

config = Config()