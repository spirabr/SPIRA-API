import inject
from fastapi import APIRouter, Depends, HTTPException, Request, status
from fastapi.encoders import jsonable_encoder
from adapters.routers.v1.utils.auth import get_header_bearer_token
from core.model.token import Token

from core.ports.authentication_port import AuthenticationPort
from core.ports.database_port import DatabasePort

from core.model.user import User
from core.model.inference import Inference, InferenceCreation, InferenceCreationForm
from core.model.exception import LogicException
from core.services.inference_service import create_new_inference, get_by_id, get_list


@inject.autoparams()
def create_inference_router(
    authentication_port: AuthenticationPort, database_port: DatabasePort
):
    router: APIRouter = APIRouter(prefix="/v1/users")

    @router.get("/{user_id}/inferences/{inference_id}", response_model=Inference)
    def get_inference_by_id(inference_id: str, user_id: str, req: Request):
        try:
            token_content = get_header_bearer_token(req)
        except:
            raise HTTPException(status.HTTP_401_UNAUTHORIZED, "Not authenticated")
        try:
            inference = get_by_id(
                authentication_port,
                database_port,
                inference_id,
                user_id,
                Token(content=token_content),
            )
        except LogicException as e:
            raise HTTPException(e.error_status, e.message)
        return inference

    @router.get("/{user_id}/inferences")
    def get_inference_list(user_id: str, req: Request):
        try:
            token_content = get_header_bearer_token(req)
        except:
            raise HTTPException(status.HTTP_401_UNAUTHORIZED, "Not authenticated")
        try:
            inference_list = get_list(
                authentication_port,
                database_port,
                user_id,
                Token(content=token_content),
            )
        except LogicException as e:
            raise HTTPException(e.error_status, e.message)
        return {"inferences": jsonable_encoder(inference_list)}

    @router.post("/{user_id}/inferences")
    def create_inference(
        user_id: str, inference_form: InferenceCreationForm, req: Request
    ):
        try:
            token_content = get_header_bearer_token(req)
        except:
            raise HTTPException(status.HTTP_401_UNAUTHORIZED, "Not authenticated")
        try:
            create_new_inference(
                authentication_port,
                database_port,
                user_id,
                inference_form,
                Token(content=token_content),
            )
        except LogicException as e:
            raise HTTPException(e.error_status, e.message)
        return {"message": "inference registered!"}

    return router
