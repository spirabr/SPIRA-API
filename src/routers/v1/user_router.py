import inject
from fastapi import APIRouter, HTTPException, status, Depends
from fastapi.encoders import jsonable_encoder
from fastapi.security import OAuth2PasswordRequestForm
from datetime import timedelta

from domain.ports.database_port import DatabasePort
from domain.model.user import User, UserForm, AuthenticationUser
from domain.model.token import Token, JWTData
from domain.services.authentication_service import AuthenticationService


@inject.autoparams()
def create_user_router(
    authentication_service: AuthenticationService, database_port: DatabasePort
):
    router: APIRouter = APIRouter(prefix="/v1/users")

    @router.get("/{user_id}")
    def get_user_by_id(user_id: str):
        try:
            user = database_port.get_user_by_id(user_id=user_id)
        except:
            raise HTTPException(status.HTTP_400_BAD_REQUEST, "user id is not valid")
        if user is None:
            raise HTTPException(status.HTTP_404_NOT_FOUND, "user not found")
        return jsonable_encoder(user.to_dict())

    @router.post("/auth", response_model=Token)
    async def authenticate_and_create_token(
        form_data: OAuth2PasswordRequestForm = Depends(),
    ):
        try:
            user = authentication_service.authenticate_user(
                form_data.username, form_data.password
            )
        except Exception as e:
            raise e
        if not user:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Incorrect username or password",
                headers={"WWW-Authenticate": "Bearer"},
            )
        access_token = authentication_service.create_access_token(
            data=JWTData(sub=user.username).dict()
        )
        return {"access_token": access_token, "token_type": "bearer"}

    @router.post("/")
    def create_user(user_form: UserForm):
        new_user = AuthenticationUser(
            username=user_form.username,
            email=user_form.email,
            hashed_password=authentication_service.get_password_hash(
                user_form.password
            ),
        )
        try:
            database_port.insert_user(new_user)
            return {"message": "user registered!"}
        except Exception as e:
            raise e
            # raise HTTPException(
            #    status_code=status.HTTP_400_BAD_REQUEST,
            #    detail="Failed to register new user",
            #    headers={"WWW-Authenticate": "Bearer"},
            # )

    return router
