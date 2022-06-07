import inject
from fastapi import APIRouter, HTTPException, status, Depends
from fastapi.encoders import jsonable_encoder
from fastapi.security import OAuth2PasswordRequestForm

from domain.ports.database_port import DatabasePort
from domain.model.user import User, UserForm, AuthenticationUser
from domain.model.token import Token, JWTData
from domain.services.authentication_service import IAuthenticationService
from domain.exceptions.base_exceptions import BaseExceptions
from domain.exceptions.entity_exceptions import UserExceptions


@inject.autoparams()
def create_user_router(
    authentication_service: IAuthenticationService, database_port: DatabasePort
):
    router: APIRouter = APIRouter(prefix="/v1/users")

    @router.get("/{user_id}")
    def get_user_by_id(
        user_id: str,
        requesting_user: User = Depends(authentication_service.get_current_user),
    ):
        try:
            user = database_port.get_user_by_id(user_id=user_id)
        except:
            raise UserExceptions.id_not_valid_exception()
        if user is None:
            raise UserExceptions.id_not_found_exception()
        return jsonable_encoder(user.dict())

    @router.post("/auth", response_model=Token)
    async def authenticate_and_create_token(
        form_data: OAuth2PasswordRequestForm = Depends(),
    ):
        try:
            user = authentication_service.authenticate_user(
                form_data.username, form_data.password
            )
        except:
            raise BaseExceptions.login_unauthorized_exception()
        if not user:
            raise BaseExceptions.login_unauthorized_exception()
        access_token = authentication_service.create_access_token(
            data=JWTData(sub=user.username).dict()
        )
        return {"access_token": access_token, "token_type": "bearer"}

    @router.post("/")
    def create_user(
        user_form: UserForm,
        requesting_user: User = Depends(authentication_service.get_current_user),
    ):
        try:
            new_user = AuthenticationUser(
                username=user_form.username,
                email=user_form.email,
                hashed_password=authentication_service.get_password_hash(
                    user_form.password
                ),
            )
            database_port.insert_user(new_user)
            return {"message": "user registered!"}
        except:
            raise UserExceptions.registry_exception()

    return router
