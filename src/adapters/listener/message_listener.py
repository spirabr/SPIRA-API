from asyncio import sleep, get_event_loop
import configparser
from core.ports.database_port import DatabasePort
from core.ports.message_service_port import MessageServicePort

from core.services.message_listener_service import listen_for_messages_and_update

cfg = configparser.ConfigParser()
cfg.read("adapters/message_listener/.cfg")


async def listen_for_messages_loop(
    message_service_port: MessageServicePort, database_port: DatabasePort
):
    for i in range(int(cfg["loop_params"]["loop_timeout"])):
        await sleep(int(cfg["loop_params"]["loop_interval"]))
        try:
            await listen_for_messages_and_update(message_service_port, database_port)
        except Exception as e:
            raise e


def run_listener(ports: dict):
    loop = get_event_loop()
    loop.run_until_complete(
        listen_for_messages_loop(ports["message_service_port"], ports["database_port"])
    )
    loop.run_forever()
    loop.close()
