from pymongo import MongoClient


class Database:

    _instances = {}

    def __new__(cls, conn_url):
        if conn_url not in cls._instances:
            cls._instances[conn_url] = super().__new__(cls)
        return cls._instances[conn_url]

    def __init__(self, conn_url):
        self._conn = MongoClient(conn_url)

    def get_conn(self):
        return self._conn

    def get_db(self, db_name):
        return getattr(self._conn, db_name)
