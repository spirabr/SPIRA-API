from typing import List, Optional
from fastapi import (
    APIRouter,
    Depends,
    HTTPException,
)
from fastapi.encoders import jsonable_encoder
from fastapi.security import OAuth2PasswordBearer
from adapters.routers.v1.utils.form_helpers import (
    get_inference_form_files,
    get_inference_form_model,
)

from core.ports.authentication_port import AuthenticationPort
from core.ports.database_port import DatabasePort
from core.model.token import Token
from core.model.inference import Inference, InferenceCreationForm, InferenceFiles
from core.model.exception import LogicException
from core.ports.message_service_port import MessageServicePort
from core.ports.simple_storage_port import SimpleStoragePort
from core.services.inference_service import create_new_inference, get_by_id, get_list
from core.services.result_service import create_inference_result


def create_inference_router(
    simple_storage_port: SimpleStoragePort,
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
    async def create_inference(
        user_id: str,
        inference_form: InferenceCreationForm = Depends(get_inference_form_model),
        inference_files: InferenceFiles = Depends(get_inference_form_files),
        token_content: str = Depends(oauth2_scheme),
    ):
        try:
            inference_id = await create_new_inference(
                simple_storage_port,
                message_service_port,
                authentication_port,
                database_port,
                user_id,
                inference_form,
                inference_files,
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
        return {"inference_id": inference_id}

    return router
