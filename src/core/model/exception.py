class LogicException(Exception):
    def __init__(self, message: str, error_status: int):
        self.message = message
        self.error_status = error_status
