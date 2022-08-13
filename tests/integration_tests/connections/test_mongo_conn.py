import pytest
from bson.objectid import ObjectId
from pymongo.collection import Collection
from pymongo import MongoClient

from adapters.database.mongo_adapter import MongoAdapter
from src.settings import Settings


@pytest.fixture()
def database_adapter():
    try:
        conn = MongoClient(Settings.database_settings.mongo_conn_url)
        conn.drop_database("test_database")
    finally:
        pass

    adapter = MongoAdapter(
        Settings.database_settings.mongo_conn_url,
        "test_database",
        Settings.database_settings.user_collection_name,
        Settings.database_settings.inference_collection_name,
        Settings.database_settings.model_collection_name,
        Settings.database_settings.result_collection_name,
    )

    yield adapter

    adapter._conn.drop_database("test_database")


def test_ping_db_connection(database_adapter: MongoAdapter):
    try:
        ret = database_adapter._db.command("ping")
        assert ret == {"ok": 1.0}
    except:
        assert False


def test_db_has_users_collection(database_adapter: MongoAdapter):
    try:
        users_collection = getattr(
            database_adapter._db, Settings.database_settings.user_collection_name
        )
        assert type(users_collection) == Collection
    except Exception as e:
        print(e, flush=True)
        assert False


def test_db_has_inferences_collection(database_adapter: MongoAdapter):
    try:
        inferences_collection = getattr(
            database_adapter._db, Settings.database_settings.inference_collection_name
        )
        assert type(inferences_collection) == Collection
    except Exception as e:
        print(e, flush=True)
        assert False


def test_db_has_models_collection(database_adapter: MongoAdapter):
    try:
        models_collection = getattr(
            database_adapter._db, Settings.database_settings.model_collection_name
        )
        assert type(models_collection) == Collection
    except Exception as e:
        print(e, flush=True)
        assert False


def test_db_has_results_collection(database_adapter: MongoAdapter):
    try:
        results_collection = getattr(
            database_adapter._db, Settings.database_settings.result_collection_name
        )
        assert type(results_collection) == Collection
    except Exception as e:
        print(e, flush=True)
        assert False
