from typing import Optional

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
