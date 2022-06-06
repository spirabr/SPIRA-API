import inject

from tests.mocks.mongo_mock import MongoMock
from tests.mocks.authentication_mock import AuthenticationServiceMock
from domain.interfaces.database_interface import DatabaseInterface
from domain.services.authentication_service import (
    IAuthenticationService,
    AuthenticationService,
)


def config_with_auth(binder: inject.Binder) -> None:
    binder.bind(DatabaseInterface, MongoMock())
    binder.bind(IAuthenticationService, AuthenticationServiceMock())


def config_without_auth(binder: inject.Binder) -> None:
    binder.bind(DatabaseInterface, MongoMock())
    binder.bind(IAuthenticationService, AuthenticationService())


def inject_dependencies(config=None) -> None:
    if config is not None:
        inject.configure(config)

    @inject.autoparams()
    def configure_injections(authentication_service: IAuthenticationService):
        authentication_service._configure_injections()

    configure_injections()
