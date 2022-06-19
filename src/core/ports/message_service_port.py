from core.model.message_service import RequestLetter
from core.model.result import ResultUpdate


class MessageServicePort:
    def __init__(self, message_service_adapter):
        self._message_service_adapter = message_service_adapter

    def send_message(self, letter: RequestLetter):
        self._message_service_adapter.send_message(
            letter.content.dict(), letter.publishing_channel
        )

    def receive_message(self, receiving_channel: str) -> ResultUpdate:
        return self._message_service_adapter.receive_message(receiving_channel)
