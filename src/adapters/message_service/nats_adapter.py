import nats
from nats.aio.client import Client


class NATSAdapter:
    @classmethod
    async def create_adapter(cls, conn_url):
        self = NATSAdapter()
        self._conn_url = conn_url
        self._nc = await nats.connect(self._conn_url)
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
