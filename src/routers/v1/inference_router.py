import inject
from fastapi import APIRouter, Depends
from fastapi.encoders import jsonable_encoder

from domain.ports.database_port import DatabasePort
from domain.model.user import User
from domain.services.authentication_service import IAuthenticationService
from domain.exceptions.base_exceptions import BaseExceptions
from domain.exceptions.entity_exceptions import InferenceExceptions


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

    return router
