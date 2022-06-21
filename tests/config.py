from core.ports.authentication_port import AuthenticationPort
from core.ports.database_port import DatabasePort
from tests.mocks.authentication_mock import (
    AuthenticationMock,
    UnauthorizedAuthenticationMock,
)
from tests.mocks.mongo_mock import MongoMock


def configure_ports_without_auth():
    ports = {}
    ports["database_port"] = DatabasePort(MongoMock())
    ports["authentication_port"] = AuthenticationPort(UnauthorizedAuthenticationMock())
    return ports


def configure_ports_with_auth():
    ports = {}
    ports["database_port"] = DatabasePort(MongoMock())
    ports["authentication_port"] = AuthenticationPort(AuthenticationMock())
    return ports
