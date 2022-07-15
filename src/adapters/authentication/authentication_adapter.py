from typing import Optional
from passlib.context import CryptContext
from datetime import datetime, timedelta
from passlib.context import CryptContext
from jose import jwt

from core.model.token import Token, TokenData


class AuthenticationAdapter:
    """Adapter for the authentication of requests

    Args:
        expire_time (int) : token expire time
        key (str) : secret key used to generate token
        algorithm (str) : algorithm used to generate token
        context_scheme (str) : encryption context scheme
        deprecated (str) : encryption context parameter

    """

    def __init__(
        self, expire_time: int, key: str, algorithm, context_scheme, deprecated
    ):
        self._pwd_context = CryptContext(
            schemes=[context_scheme], deprecated=deprecated
        )
        self._expire_time = expire_time
        self._key = key
        self._algorithm = algorithm

    def get_password_hash(self, plain_password: str) -> str:
        """gets the plain password hash value

        Args:
            plain_password (str) : plain password

        Returns:
            hashed password

        """
        return self._pwd_context.hash(plain_password)

    def verify_password(self, plain_password: str, user_password: str) -> bool:
        """verifies if the plain password matches with the user hashed password

        Args:
            plain_password (str) : plain password
            user_password (str) : user hashed password

        Returns:
            True if they match. False otherwise

        """
        return self._pwd_context.verify(plain_password, user_password)

    def generate_token(self, data: TokenData) -> Token:
        """generates the jwt token

        Args:
            data (TokenData) : data object with the info to be encoded in the token

        Returns:
            JWT token with the data encoded

        """
        to_encode = data.dict().copy()
        expire = datetime.utcnow() + timedelta(minutes=self._expire_time)
        to_encode.update({"exp": expire})
        encoded_jwt = jwt.encode(
            to_encode,
            self._key,
            algorithm=self._algorithm,
        )
        return Token(content=encoded_jwt)

    def validate_token(self, token: Token) -> bool:
        """validates the token

        Args:
            token (Token) : token object

        Returns:
            True if it is valid. False otherwise

        """
        try:
            jwt.decode(
                token.content,
                self._key,
                algorithms=[self._algorithm],
            )
        except:
            return False
        return True

    def decode_token(self, token: Token) -> Optional[TokenData]:
        """decodes the token

        Args:
            token (Token) : token object

        Returns:
            returns the decoded token data, if it is valid.

        Raises:
            invalid token exception, if it is not valid.

        """
        try:
            payload = jwt.decode(
                token.content,
                self._key,
                algorithms=[self._algorithm],
            )
            username: str = payload.get("username")
        except:
            raise
        return TokenData(username=username)
