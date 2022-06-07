from fastapi import status, HTTPException


class BaseExceptions:
    @classmethod
    def get_unauthorized_exception(cls):
        return HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="could not validate credentials",
            headers={"WWW-Authenticate": "Bearer"},
        )

    @classmethod
    def get_login_unauthorized_exception(cls):
        return HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="invalid username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )

    @classmethod
    def get_forbidden_exception(cls):
        return HTTPException(
            status_code=status.HTTP_403_FORBIDDEN, detail="Forbidden operation"
        )
