import json

from core.model.message_service import RequestLetter
from core.model.result import ResultUpdate


class MessageServicePort:
    def __init__(self, message_service_adapter):
        self._message_service_adapter = message_service_adapter

    async def send_message(self, letter: RequestLetter):
        await self._message_service_adapter.send_message(
            json.dumps(letter.content.dict()), letter.publishing_channel
        )

    async def subscribe(self, receiving_channel: str):
        await self._message_service_adapter.subscribe(receiving_channel)

    async def wait_for_message(self, receiving_channel: str) -> ResultUpdate:
        message_dict = json.loads(
            await self._message_service_adapter.wait_for_message(receiving_channel)
        )
        return ResultUpdate(**message_dict)
