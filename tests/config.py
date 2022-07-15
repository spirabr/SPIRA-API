from adapters.message_service.nats_adapter import NATSAdapter
from core.ports.authentication_port import AuthenticationPort
from core.ports.database_port import DatabasePort
from core.ports.message_service_port import MessageServicePort
from core.ports.ports import Ports
from core.ports.simple_storage_port import SimpleStoragePort
from tests.mocks.authentication_mock import (
    AuthenticationMock,
    UnauthorizedAuthenticationMock,
)
from tests.mocks.minio_mock import MinioMock
from tests.mocks.mongo_mock import MongoMock
from tests.mocks.nats_mock import NATSMock


def configure_ports_without_auth() -> Ports:
    ports = Ports(
        DatabasePort(MongoMock()),
        MessageServicePort(NATSMock()),
        AuthenticationPort(UnauthorizedAuthenticationMock()),
        SimpleStoragePort(MinioMock()),
    )
    return ports


def configure_ports_with_auth() -> Ports:
    ports = Ports(
        DatabasePort(MongoMock()),
        MessageServicePort(NATSMock()),
        AuthenticationPort(AuthenticationMock()),
        SimpleStoragePort(MinioMock()),
    )
    return ports
