import asyncio
import nats
from nats.aio.client import Client


class NATSAdapter:
    def __init__(self, conn_url):
        self._conn_url = conn_url
        self._nc: Client = Client()
        self._receiving_nc = Client()
        print("client connected", flush=True)
        self._subs = {}

    async def send_message(self, message: dict, publishing_topic: str):
        await self._nc.connect(
            self._conn_url,
            ping_interval=1,
            allow_reconnect=True,
        )
        await self._nc.publish(
            publishing_topic, str.encode(str(message), encoding="utf-8")
        )
        await self._nc.close()

    async def subscribe(self, receiving_channel: str):
        print("subscribing to ", receiving_channel, flush=True)

        self._receiving_nc = await nats.connect(
            self._conn_url,
            ping_interval=1,
            allow_reconnect=True,
        )
        self._subs[receiving_channel] = await self._receiving_nc.subscribe(
            receiving_channel
        )
        await self._receiving_nc.flush(timeout=5)

    async def wait_for_message(self, receiving_channel: str):
        print("waiting for next msg...", flush=True)
        while True:
            try:
                msg = await self._subs[receiving_channel].next_msg()
                return msg.data.decode("utf-8")
            except:
                continue
