from fastapi import Depends

from src.domain.model.user import User, AuthenticationUser
from src.domain.model.token import TokenData
from src.domain.ports.database_port import DatabasePort
from src.domain.services.authentication_service import IAuthenticationService


class AuthenticationServiceMock(IAuthenticationService):
    def __init__(self):
        pass

    def _configure_injections(self):
        pass

    def get_password_hash(self, password: str):
        return "fake_password_hash"

    def verify_password(self, plain_password: str, hashed_password: str):
        pass

    def authenticate_user(
        self,
        username: str,
        password: str,
    ) -> AuthenticationUser:
        pass

    def create_access_token(self, data: dict):
        pass

    async def get_current_user(self) -> User:
        return User(
            id="507f191e810c19729de860ea", username="fake_username", email="fake_email"
        )
