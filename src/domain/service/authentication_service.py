from passlib.context import CryptContext
from fastapi.security import OAuth2PasswordBearer
from fastapi import Depends, status, HTTPException
from datetime import datetime, timedelta
from passlib.context import CryptContext
from typing import Union
from jose import JWTError, jwt
from configparser import ConfigParser
import inject


from domain.model.user import User, AuthenticationUser
from domain.model.token import TokenData
from domain.ports.database_port import DatabasePort

cfg = ConfigParser()
cfg.read("domain/database/.cfg")


class AuthenticationService:

    pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
    oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")

    @inject.autoparams()
    def __init__(self, database_port: DatabasePort):
        self._database_port = database_port

    def get_password_hash(self, password: str):
        return self.pwd_context.hash(password)

    def verify_password(self, plain_password: str, hashed_password: str):
        return self.pwd_context.verify(plain_password, hashed_password)

    def authenticate_user(
        self,
        user_id: str,
        password: str,
    ) -> AuthenticationUser:
        user = self._database_port.get_auth_user_by_id(user_id)
        if user is None:
            return False
        if not self.verify_password(password, user.hashed_password):
            return False
        return user

    def validate_new_user(self, user: User):
        return True, 400

    def create_access_token(
        self, data: dict, expires_delta: Union[timedelta, None] = None
    ):
        to_encode = data.copy()
        if expires_delta:
            expire = datetime.utcnow() + expires_delta
        else:
            expire = datetime.utcnow() + timedelta(minutes=15)
        to_encode.update({"exp": expire})
        encoded_jwt = jwt.encode(
            to_encode, cfg["token"]["key"], algorithm=cfg["token"]["algorithm"]
        )
        return encoded_jwt

    async def get_current_user(self, token: str = Depends(oauth2_scheme)) -> User:
        credentials_exception = HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Could not validate credentials",
            headers={"WWW-Authenticate": "Bearer"},
        )
        try:
            payload = jwt.decode(
                token, cfg["token"]["key"], algorithm=cfg["token"]["algorithm"]
            )
            username: str = payload.get("sub")
            if username is None:
                raise credentials_exception
            token_data = TokenData(username=username)
        except JWTError:
            raise credentials_exception
        user = self._database_port.get_user_by_username(token_data.username)
        if user is None:
            raise credentials_exception
        return user

    async def check_user(self, user_id: str, user: User = Depends(get_current_user)):
        if user.id != user_id:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="Forbidden operation",
                headers={"WWW-Authenticate": "Bearer"},
            )
        return user
