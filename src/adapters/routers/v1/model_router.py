import inject
from fastapi import APIRouter, Depends, HTTPException, status, Request
from fastapi.encoders import jsonable_encoder
from fastapi.security import OAuth2PasswordBearer
from core.model.token import Token

from core.model.user import User
from core.ports.authentication_port import AuthenticationPort
from core.ports.database_port import DatabasePort
from core.services.model_service import get_by_id, get_list
from core.model.exception import LogicException


@inject.autoparams()
def create_model_router(
    authentication_port: AuthenticationPort,
    database_port: DatabasePort,
    oauth2_scheme: OAuth2PasswordBearer,
):
    router: APIRouter = APIRouter(prefix="/v1/models")

    @router.get("/{model_id}")
    def get_model_by_id(model_id: str, token_content: str = Depends(oauth2_scheme)):
        try:
            model = get_by_id(
                authentication_port,
                database_port,
                model_id,
                Token(content=token_content),
            )
        except LogicException as e:
            raise HTTPException(e.error_status, e.message)
        return jsonable_encoder(model.dict())

    @router.get("/")
    def get_model_list(token_content: str = Depends(oauth2_scheme)):
        try:
            model_list = get_list(
                authentication_port, database_port, Token(content=token_content)
            )
        except LogicException as e:
            raise HTTPException(e.error_status, e.message)
        return {"models": jsonable_encoder(model_list)}

    return router
