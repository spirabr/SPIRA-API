import os

import inject
from fastapi import FastAPI
from websockets import Data

from tests.mocks.mongo_mock import MongoMock
from domain.interfaces.database_interface import DatabaseInterface


def inject_dependencies() -> None:
    def config(binder: inject.Binder) -> None:
        binder.bind(DatabaseInterface, MongoMock())

    inject.configure(config)
