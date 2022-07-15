import json

from core.model.message_service import RequestLetter
from core.model.result import ResultUpdate


class MessageServicePort:
    """Port for the message service

    Args:
        message_service_adapter (Adapter Class) : message service adapter instance

    """

    def __init__(self, message_service_adapter):
        self._message_service_adapter = message_service_adapter

    async def send_message(self, letter: RequestLetter):
        """sends a serialized json to the message service

        Args:
            letter (RequestLetter) : object containing message and publishing channel

        Returns:
            None

        """
        await self._message_service_adapter.send_message(
            json.dumps(letter.content.dict()), letter.publishing_channel
        )

    async def subscribe(self, receiving_channel: str):
        """subscribes to the channel to receive messages from it

        Args:
            receiving_channel (str) : receiving channel

        Returns:
            None

        """
        await self._message_service_adapter.subscribe(receiving_channel)

    async def wait_for_message(self, receiving_channel: str) -> ResultUpdate:
        """waits until a message arrives in the given channel from the message service

        Args:
            receiving_channel (str) : channel to listen

        Returns:
            result update form

        """
        message_dict = json.loads(
            await self._message_service_adapter.wait_for_message(receiving_channel)
        )
        return ResultUpdate(**message_dict)
