import asyncio
import nats
from nats.aio.client import Client
import logging


class NATSAdapter:
    """Adapter for the NATS server

    Args:
        nats_conn_url (str) : connection url to NATS server container

    """

    def __init__(self, conn_url: str):
        self._conn_url = conn_url
        self._nc = Client()
        self._receiving_nc = Client()
        self._subs: dict = {}

    async def send_message(self, message: str, publishing_topic: str):
        """sends a message in the given topic

        Args:
            message (str) : message to be sent
            publishing_topic (str) : publishing topic

        Returns:
            None

        """
        await self._nc.connect(
            self._conn_url,
            ping_interval=1,
            allow_reconnect=True,
        )

        await self._nc.publish(publishing_topic, str.encode(message, encoding="utf-8"))
        await self._nc.close()

    async def subscribe(self, receiving_topic: str):
        """subscribes to a topic

        Args:
            receiving_topic (str) : topic to subscribe in

        Returns:
            None

        """
        await self._receiving_nc.connect(
            self._conn_url,
            ping_interval=1,
            allow_reconnect=True,
        )
        self._subs[receiving_topic] = await self._receiving_nc.subscribe(
            receiving_topic
        )
        await self._receiving_nc.flush(timeout=5)

    async def wait_for_message(self, receiving_topic: str):
        """waits until a message arrives in the given topic

        Args:
            receiving_topic (str) : topic to listen

        Returns:
            serialized json of the arrived message

        """
        while True:
            try:
                msg = await self._subs[receiving_topic].next_msg()
                return msg.data.decode("utf-8")
            except:
                continue
