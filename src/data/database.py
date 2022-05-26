from typing import Dict
from pymongo import MongoClient
from pymongo.database import Database


class Database_Connection:

    _instances: Dict[str, "Database_Connection"] = {}

    def __new__(cls, conn_url: str) -> "Database_Connection":
        if conn_url not in cls._instances:
            cls._instances[conn_url] = super().__new__(cls)
        return cls._instances[conn_url]

    def __init__(self, conn_url) -> None:
        self._conn: MongoClient = MongoClient(conn_url)

    def get_conn(self) -> MongoClient:
        return self._conn

    def get_db(self, db_name: str) -> Database:
        return getattr(self._conn, db_name)
