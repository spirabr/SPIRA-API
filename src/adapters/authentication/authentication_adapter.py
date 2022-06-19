import configparser
from typing import Optional
from passlib.context import CryptContext
from fastapi.security import OAuth2PasswordBearer
from datetime import datetime, timedelta
from passlib.context import CryptContext
from jose import jwt

from core.model.token import Token, TokenData

cfg = configparser.ConfigParser()
cfg.read("adapters/authentication/.cfg")


class AuthenticationAdapter:
    def __init__(self):
        self._pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

    def get_password_hash(self, plain_password: str) -> str:
        return self._pwd_context.hash(plain_password)

    def verify_password(self, plain_password: str, user_password: str) -> bool:
        return self._pwd_context.verify(plain_password, user_password)

    def generate_token(self, data: TokenData) -> Token:
        to_encode = data.dict().copy()
        expire = datetime.utcnow() + timedelta(minutes=int(cfg["token"]["expire_time"]))
        to_encode.update({"exp": expire})
        encoded_jwt = jwt.encode(
            to_encode,
            cfg["token"]["key"],
            algorithm=cfg["token"]["algorithm"],
        )
        return Token(content=encoded_jwt)

    def validate_token(self, token: Token) -> bool:
        try:
            jwt.decode(
                token.content,
                cfg["token"]["key"],
                algorithms=[cfg["token"]["algorithm"]],
            )
        except:
            return False
        return True

    def decode_token(self, token: Token) -> Optional[TokenData]:
        try:
            payload = jwt.decode(
                token.content,
                cfg["token"]["key"],
                algorithms=[cfg["token"]["algorithm"]],
            )
            username: str = payload.get("username")
        except:
            raise
        return TokenData(username=username)
