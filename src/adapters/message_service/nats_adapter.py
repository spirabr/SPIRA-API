from nats.aio.client import Client


class NATSAdapter:
    def __init__(self, conn_url):
        self._conn_url = conn_url
        self._nc: Client = Client()

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

    # async def receive_message(self, receiving_channel: str) -> str:
    #     return (await self._nc.request(receiving_channel)).data.decode("utf-8")
