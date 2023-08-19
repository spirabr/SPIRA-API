import logging
from threading import Thread
from adapters.authentication.authentication_adapter import AuthenticationAdapter
from adapters.database.mongo_adapter import MongoAdapter
from adapters.message_service.nats_adapter import NATSAdapter
from adapters.simple_storage.minio_adapter import MinioAdapter

from core.ports.authentication_port import AuthenticationPort
from core.ports.database_port import DatabasePort
from core.ports.message_service_port import MessageServicePort

from adapters.routers.app import run_app
from adapters.listener.message_listener import run_listener
from core.ports.ports import Ports
from core.ports.simple_storage_port import SimpleStoragePort
from settings import (
    Settings,
)


def configure_ports() -> Ports:
    """Instantiates Ports and Adapters of the services used in the application

    Args:
        None

    Returns:
        Ports object with port instances as attributes

    """
    ports = Ports(
        DatabasePort(
            MongoAdapter(
                Settings.database_settings.M_CONN_URL,
                Settings.database_settings.DATABASE_NAME,
                Settings.database_settings.user_collection_name,
                Settings.database_settings.inference_collection_name,
                Settings.database_settings.model_collection_name,
                Settings.database_settings.result_collection_name,
            )
        ),
        MessageServicePort(
            NATSAdapter(
                Settings.message_service_settings.nats_conn_url,
            )
        ),
        AuthenticationPort(
            AuthenticationAdapter(
                Settings.authentication_settings.expire_time,
                Settings.authentication_settings.key,
                Settings.authentication_settings.algorithm,
                Settings.authentication_settings.context_scheme,
                Settings.authentication_settings.deprecated,
            )
        ),
        SimpleStoragePort(
            MinioAdapter(
                Settings.simple_storage_settings.minio_conn_url,
                Settings.simple_storage_settings.minio_access_key,
                Settings.simple_storage_settings.minio_secret_key,
                Settings.simple_storage_settings.bucket_name,
                Settings.simple_storage_settings.file_extension,
            )
        ),
    )
    return ports


def create_app_process(ports: Ports) -> Thread:
    """Creates the thread for the API app process

    Args:
        ports (Ports): Ports object with ports instances

    Returns:
        Thread object with the app process

    """
    app_process = Thread(target=run_app, args=(ports,))
    return app_process


def create_listener_process(ports: Ports):
    """Creates the thread for the message listener process

    Args:
        ports (Ports): Ports object with ports instances

    Returns:
        Thread object with the listener process

    """
    listener_process = Thread(target=run_listener, args=(ports,))
    return listener_process


if __name__ == "__main__":
    ports = configure_ports()
    logging.info("starting both processes...")
    app_process = create_app_process(ports)
    listener_process = create_listener_process(ports)

    app_process.start()
    listener_process.start()
