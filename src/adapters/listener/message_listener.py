from asyncio import sleep, get_event_loop
import asyncio
from core.ports.database_port import DatabasePort
from core.ports.message_service_port import MessageServicePort
from core.ports.ports import Ports
from core.ports.simple_storage_port import SimpleStoragePort

from core.services.message_listener_service import (
    listen_for_messages_and_update,
    subscribe_to_channel,
)
from settings import Settings


async def listen_for_messages_loop(
    simple_storage_port: SimpleStoragePort,
    message_service_port: MessageServicePort,
    database_port: DatabasePort,
):
    try:
        await subscribe_to_channel(
            message_service_port, Settings.message_listener_settings.central_channel
        )
    except Exception as e:
        print(e, flush=True)

    while True:
        await sleep(Settings.message_listener_settings.loop_interval)
        try:
            await listen_for_messages_and_update(
                simple_storage_port,
                message_service_port,
                database_port,
                Settings.message_listener_settings.central_channel,
            )
        except Exception as e:
            print(e, flush=True)


def run_listener(ports: Ports):
    asyncio.new_event_loop().run_until_complete(
        listen_for_messages_loop(
            ports.simple_storage_port,
            ports.message_service_port,
            ports.database_port,
        )
    )
