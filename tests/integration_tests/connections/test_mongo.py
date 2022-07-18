import pytest

from adapters.database.mongo_adapter import MongoAdapter


@pytest.fixture()
def database_adapter():

    # MongoMock inherits all methods from MongoAdapter
    # but uses a mocked client with the DB

    adapter = MongoAdapter()
    return adapter
