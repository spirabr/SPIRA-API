import os

import inject
from fastapi import FastAPI
from websockets import Data

from adapters.database.mongo import MongoAdapter
from domain.interfaces.database_interface import DatabaseInterface
from domain.services.authentication_service import (
    IAuthenticationService,
    AuthenticationService,
)


def inject_dependencies() -> None:
    def config(binder: inject.Binder) -> None:
        binder.bind(DatabaseInterface, MongoAdapter())

        binder.bind(IAuthenticationService, AuthenticationService())

    inject.configure(config)

    @inject.autoparams()
    def configure_injections(authentication_service: IAuthenticationService):
        authentication_service._configure_injections()

    configure_injections()
