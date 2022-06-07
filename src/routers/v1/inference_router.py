import inject
from fastapi import APIRouter, Depends
from fastapi.encoders import jsonable_encoder

from domain.ports.database_port import DatabasePort
from domain.model.user import User
from domain.model.inference import Inference, InferenceForm
from domain.services.authentication_service import IAuthenticationService
from domain.exceptions.base_exceptions import BaseExceptions
from domain.exceptions.entity_exceptions import InferenceExceptions, ModelExceptions


@inject.autoparams()
def create_inference_router(
    authentication_service: IAuthenticationService, database_port: DatabasePort
):
    router: APIRouter = APIRouter(prefix="/v1/users")

    @router.get("/{user_id}/inferences/{inference_id}")
    def get_inference_by_id(
        inference_id: str,
        user_id: str,
        requesting_user: User = Depends(authentication_service.get_current_user),
    ):
        if requesting_user.id != user_id:
            raise BaseExceptions.get_forbidden_exception()
        try:
            inference = database_port.get_inference_by_id(inference_id=inference_id)
        except:
            raise InferenceExceptions.get_id_not_valid_exception()
        if inference is None:
            raise InferenceExceptions.get_id_not_found_exception()
        if inference.user_id != user_id:
            raise BaseExceptions.get_forbidden_exception()
        return jsonable_encoder(inference.dict())

    @router.post("/{user_id}/inferences")
    def create_inference(
        inference_form: InferenceForm,
        user_id: str,
        requesting_user: User = Depends(authentication_service.get_current_user),
    ):
        if requesting_user.id != user_id:
            raise BaseExceptions.get_forbidden_exception()
        try:
            model = database_port.get_model_by_id(model_id=inference_form.model_id)
        except:
            raise ModelExceptions.get_id_not_valid_exception()
        if model is None:
            raise ModelExceptions.get_id_not_found_exception()
        try:
            new_inference = Inference(
                age=inference_form.age,
                sex=inference_form.sex,
                user_id=user_id,
                model_id=inference_form.model_id,
            )
            database_port.insert_inference(new_inference)
            return {"message": "inference registered!"}
        except:
            raise InferenceExceptions.get_registry_exception()

    @router.get("/{user_id}/inferences")
    def get_inference_list(
        user_id: str,
        requesting_user: User = Depends(authentication_service.get_current_user),
    ):
        if requesting_user.id != user_id:
            raise BaseExceptions.get_forbidden_exception()
        try:
            inference_list = database_port.get_inference_list_by_user_id(
                user_id=user_id
            )
            return jsonable_encoder({"inferences": inference_list})
        except Exception as e:
            raise e

    return router
