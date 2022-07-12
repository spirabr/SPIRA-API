from threading import Thread
from adapters.authentication.authentication_adapter import AuthenticationAdapter
from adapters.database.mongo_adapter import MongoAdapter
from adapters.message_service.nats_adapter import NATSAdapter

from core.ports.authentication_port import AuthenticationPort
from core.ports.database_port import DatabasePort
from core.ports.message_service_port import MessageServicePort

from adapters.routers.app import run_app
from adapters.listener.message_listener import run_listener
from core.ports.simple_storage_port import SimpleStoragePort
from settings import (
    Settings,
)


def configure_ports():
    ports = {}
    ports["database_port"] = DatabasePort(
        MongoAdapter(
            Settings.database_settings.mongo_conn_url,
            Settings.database_settings.database_name,
            Settings.database_settings.user_collection_name,
            Settings.database_settings.inference_collection_name,
            Settings.database_settings.model_collection_name,
            Settings.database_settings.result_collection_name,
        )
    )
    ports["authentication_port"] = AuthenticationPort(
        AuthenticationAdapter(
            Settings.authentication_settings.expire_time,
            Settings.authentication_settings.key,
            Settings.authentication_settings.algorithm,
            Settings.authentication_settings.context_scheme,
            Settings.authentication_settings.deprecated,
        )
    )
    ports["message_service_port"] = MessageServicePort(
        NATSAdapter(
            Settings.message_service_settings.nats_conn_url,
        )
    )
    ports["simple_storage_port"] = SimpleStoragePort()
    return ports


def create_app_process(ports: dict):
    app_process = Thread(target=run_app, args=(ports,))
    return app_process


def create_listener_process(ports: dict):
    listener_process = Thread(target=run_listener, args=(ports,))
    return listener_process


if __name__ == "__main__":
    ports = configure_ports()
    print("starting both processes...", flush=True)
    app_process = create_app_process(ports)
    listener_process = create_listener_process(ports)

    app_process.start()
    listener_process.start()
