from fastapi import APIRouter, HTTPException, Request, Depends, status
from fastapi.security import OAuth2PasswordRequestForm
from fastapi.encoders import jsonable_encoder
from adapters.routers.v1.utils.auth import get_header_bearer_token
from core.model.user import User, UserCreationForm
from core.ports.authentication_port import AuthenticationPort

from core.ports.database_port import DatabasePort
from core.services.user_service import (
    get_by_id,
    authenticate_and_generate_token,
    create_new_user,
)
from core.model.exception import LogicException
from core.model.token import Token


def create_user_router(
    authentication_port: AuthenticationPort, database_port: DatabasePort
):
    router: APIRouter = APIRouter(prefix="/v1/users")

    @router.get("/{user_id}", response_model=User)
    def get_user_by_id(user_id: str, req: Request):
        try:
            token_content = get_header_bearer_token(req)
        except:
            raise HTTPException(status.HTTP_401_UNAUTHORIZED, "Not authenticated")

        try:
            user = get_by_id(
                authentication_port,
                database_port,
                user_id,
                Token(content=token_content),
            )
        except LogicException as e:
            raise HTTPException(e.error_status, e.message)
        return user

    @router.post("/auth")
    async def authenticate_and_create_token(
        form_data: OAuth2PasswordRequestForm = Depends(),
    ):
        try:
            access_token = authenticate_and_generate_token(
                authentication_port,
                database_port,
                form_data.username,
                form_data.password,
            )
        except LogicException as e:
            raise HTTPException(e.error_status, e.message)
        return {"access_token": access_token.content, "token_type": "bearer"}

    @router.post("/")
    def create_user(user_form: UserCreationForm, req: Request):
        try:
            token_content = get_header_bearer_token(req)
        except:
            raise HTTPException(status.HTTP_401_UNAUTHORIZED, "Not authenticated")
        try:
            create_new_user(
                authentication_port,
                database_port,
                user_form,
                Token(content=token_content),
            )
        except LogicException as e:
            raise HTTPException(e.error_status, e.message)
        return {"message": "user registered!"}

    return router
