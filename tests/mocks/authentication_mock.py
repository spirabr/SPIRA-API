from typing import Optional
from passlib.context import CryptContext

from src.adapters.authentication.authentication_adapter import AuthenticationAdapter
from src.core.model.token import Token, TokenData


class AuthenticationMock(AuthenticationAdapter):
    def __init__(self):
        pass

    def verify_password(self, plain_password: str, user_password: str):
        return True

    def get_password_hash(self, plain_password: str) -> str:
        return "fake_hash"

    def generate_token(self, data: TokenData) -> Token:
        return Token(content="fake_token_content")

    def validate_token(self, token: Token) -> bool:
        return True

    def decode_token(self, token: Token) -> Optional[TokenData]:
        return TokenData(username="test_username")


class UnauthorizedAuthenticationMock(AuthenticationAdapter):
    def __init__(self):
        pass

    def verify_password(self, plain_password: str, user_password: str):
        return True

    def get_password_hash(self, plain_password: str) -> str:
        return "fake_hash"

    def generate_token(self, data: TokenData) -> Token:
        return Token(content="fake_token_content")

    def validate_token(self, token: Token) -> bool:
        return False

    def decode_token(self, token: Token) -> Optional[TokenData]:
        raise


class AuthenticationJWTMock(AuthenticationAdapter):
    def __init__(self):
        self._pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
        self._expire_time = 1
        self._key = "fake_secret"
        self._algorithm = "fake_algorithm"
