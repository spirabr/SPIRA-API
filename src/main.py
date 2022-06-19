from multiprocessing import Process

from adapters.authentication.authentication_adapter import AuthenticationAdapter
from adapters.database.mongo_adapter import MongoAdapter
from adapters.message_service.nats_adapter import NATSAdapter

from core.ports.authentication_port import AuthenticationPort
from core.ports.database_port import DatabasePort
from core.ports.message_service_port import MessageServicePort

from adapters.routers.app import run_app
from adapters.listener.message_listener import run_listener


def configure_ports():
    ports = {}
    ports["database_port"] = DatabasePort(MongoAdapter())
    ports["authentication_port"] = AuthenticationPort(AuthenticationAdapter())
    ports["message_service_port"] = MessageServicePort(NATSAdapter())
    return ports


def create_app_process(ports: dict):
    app_process = Process(target=run_app, args=(ports,))
    return app_process


def create_listener_process(ports: dict):
    listener_process = Process(target=run_listener, args=(ports,))
    return listener_process


if __name__ == "__main__":
    ports = configure_ports()
    app_process = create_app_process(ports)
    listener_process = create_listener_process(ports)

    app_process.run()
    listener_process.run()
