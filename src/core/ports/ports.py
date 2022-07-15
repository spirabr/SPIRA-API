from core.ports.authentication_port import AuthenticationPort
from core.ports.database_port import DatabasePort
from core.ports.message_service_port import MessageServicePort
from core.ports.simple_storage_port import SimpleStoragePort


class Ports:
    def __init__(
        self,
        database_port: DatabasePort,
        message_service_port: MessageServicePort,
        authentication_port: AuthenticationPort,
        simple_storage_port: SimpleStoragePort,
    ):
        self.database_port = database_port
        self.message_service_port = message_service_port
        self.authentication_port = authentication_port
        self.simple_storage_port = simple_storage_port
