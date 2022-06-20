import nats
from nats.aio.client import Client
import configparser

import logging

cfg = configparser.ConfigParser()
cfg.read("adapters/message_service/.cfg")


class NATSAdapter:
    @classmethod
    async def create_adapter(cls):
        self = NATSAdapter()
        self._conn_url = cfg["broker"]["conn_url"]
        logging.debug(self._conn_url)
        self._nc = await nats.connect(self._conn_url)
        logging.debug("Connected to nats!")
        return self

    def __init__(self):
        self._conn_url = ""
        self._nc: Client = None

    async def send_message(self, message: dict, publishing_topic: str):
        await self._nc.publish(
            publishing_topic, str.encode(str(message), encoding="utf-8")
        )

    async def receive_message(self, receiving_channel: str) -> str:
        return (await self._nc.request(receiving_channel)).data.decode("utf-8")
