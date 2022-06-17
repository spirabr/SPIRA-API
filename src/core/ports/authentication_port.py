from typing import Optional
from core.model.token import Token, TokenData
from core.model.user import User


class AuthenticationPort:
    def __init__(self, authentication_adapter):
        self._authentication_adapter = authentication_adapter

    def validate_token(self, token: Token):
        return self._authentication_adapter.validate_token(token)

    def generate_token(self, data: TokenData) -> Token:
        return self._authentication_adapter.generate_token(data)

    def decode_token(self, token: Token) -> Optional[TokenData]:
        return self._authentication_adapter.decode_token(token)

    def verify_password(self, plain_password: str, user_password: str) -> bool:
        return self._authentication_adapter.verify_password(
            plain_password, user_password
        )

    def get_password_hash(self, plain_password: str) -> str:
        return self._authentication_adapter.get_password_hash(plain_password)
