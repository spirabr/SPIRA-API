import os

import inject
from fastapi import FastAPI
from websockets import Data

from adapters.database.mongo import MongoAdapter
from domain.ports.database_interface import DatabaseInterface


def inject_dependencies() -> None:
    def config(binder: inject.Binder) -> None:
        binder.bind(DatabaseInterface, MongoAdapter())

    inject.configure(config)
