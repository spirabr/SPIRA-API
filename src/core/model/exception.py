from fastapi import status


class LogicException(Exception):
    def __init__(self, message: str, error_status: int):
        self.message = message
        self.error_status = error_status


class DefaultExceptions:

    credentials_exception = LogicException(
        "could not validate the credentials", status.HTTP_401_UNAUTHORIZED
    )

    forbidden_exception = LogicException(
        "Forbidden operation", status.HTTP_403_FORBIDDEN
    )

    user_form_exception = LogicException(
        "Incorrect username or password", status.HTTP_401_UNAUTHORIZED
    )
