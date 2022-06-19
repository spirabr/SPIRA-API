from core.model.result import ResultUpdate


class NATSAdapter:
    def __init__(self):
        pass

    def send_message(self, message: dict, publishing_topic: str):
        # to be implemented
        pass

    def receive_message(self, receiving_channel: str) -> ResultUpdate:
        # temporary mock
        return ResultUpdate(inference_id="fake_id", output=0.5, diagnosis="negative")
