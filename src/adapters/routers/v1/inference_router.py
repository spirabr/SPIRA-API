from fastapi import APIRouter, Depends, HTTPException, Request, status
from fastapi.encoders import jsonable_encoder
from fastapi.security import OAuth2PasswordBearer

from core.ports.authentication_port import AuthenticationPort
from core.ports.database_port import DatabasePort
from core.model.token import Token
from core.model.inference import Inference, InferenceCreationForm
from core.model.exception import LogicException
from core.ports.message_service_port import MessageServicePort
from core.services.inference_service import create_new_inference, get_by_id, get_list
from core.services.result_service import create_inference_result


def create_inference_router(
    message_service_port: MessageServicePort,
    authentication_port: AuthenticationPort,
    database_port: DatabasePort,
    oauth2_scheme: OAuth2PasswordBearer,
):
    router: APIRouter = APIRouter(prefix="/v1/users")

    @router.get("/{user_id}/inferences/{inference_id}", response_model=Inference)
    def get_inference_by_id(
        inference_id: str, user_id: str, token_content: str = Depends(oauth2_scheme)
    ):
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
    def get_inference_list(user_id: str, token_content: str = Depends(oauth2_scheme)):
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
        user_id: str,
        inference_form: InferenceCreationForm,
        token_content: str = Depends(oauth2_scheme),
    ):
        try:

            inference_id = create_new_inference(
                message_service_port,
                authentication_port,
                database_port,
                user_id,
                inference_form,
                Token(content=token_content),
            )

            create_inference_result(
                authentication_port,
                database_port,
                user_id,
                inference_id,
                Token(content=token_content),
            )
        except LogicException as e:
            raise HTTPException(e.error_status, e.message)
        return {"message": "inference registered!"}

    return router
