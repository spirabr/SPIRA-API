from typing import Optional
from core.model.token import Token, TokenData
from core.model.user import User


class AuthenticationPort:
    """Port for the authentication service

    Args:
        authentication_adapter (Adapter Class) : authentication adapter instance

    """

    def __init__(self, authentication_adapter):
        self._authentication_adapter = authentication_adapter

    def validate_token(self, token: Token) -> bool:
        """calls the adapter to validate the token

        Args:
            token (Token) : token object

        Returns:
            True if it is valid. False otherwise

        """
        return self._authentication_adapter.validate_token(token)

    def generate_token(self, data: TokenData) -> Token:
        """calls the adapter to generate the jwt token

        Args:
            data (TokenData) : data object with the info to be encoded in the token

        Returns:
            JWT token with the data encoded

        """
        return self._authentication_adapter.generate_token(data)

    def decode_token(self, token: Token) -> Optional[TokenData]:
        """calls the adapter to decode the token

        Args:
            token (Token) : token object

        Returns:
            returns the decoded token data, if it is valid.

        Raises:
            invalid token exception, if it is not valid.

        """
        return self._authentication_adapter.decode_token(token)

    def verify_password(self, plain_password: str, user_password: str) -> bool:
        """calls the adapter to verify if the plain password matches with the user hashed password

        Args:
            plain_password (str) : plain password
            user_password (str) : user hashed password

        Returns:
            True if they match. False otherwise

        """
        return self._authentication_adapter.verify_password(
            plain_password, user_password
        )

    def get_password_hash(self, plain_password: str) -> str:
        """calls the adapter to get the plain password hash value

        Args:
            plain_password (str) : plain password

        Returns:
            hashed password

        """
        return self._authentication_adapter.get_password_hash(plain_password)
