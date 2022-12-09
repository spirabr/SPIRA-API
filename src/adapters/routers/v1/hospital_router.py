from fastapi import APIRouter, Depends, HTTPException, status, Request
from fastapi.encoders import jsonable_encoder
from fastapi.security import OAuth2PasswordBearer

from core.model.token import Token
from core.model.user import User
from core.services.hospital_service import get_list
from core.model.exception import LogicException
from core.ports.authentication_port import AuthenticationPort
from core.ports.database_port import DatabasePort


def create_hospital_router(
    authentication_port: AuthenticationPort,
    database_port: DatabasePort,
    oauth2_scheme: OAuth2PasswordBearer,
):
    router: APIRouter = APIRouter(prefix="/v1/hospitals")

    @router.get("/")
    def get_hospital_list(token_content: str = Depends(oauth2_scheme)):
        try:
            hospital_list = get_list(
                authentication_port, database_port, Token(content=token_content)
            )
        except LogicException as e:
            raise HTTPException(e.error_status, e.message)
        return {"hospitals": jsonable_encoder(hospital_list)}

    return router
