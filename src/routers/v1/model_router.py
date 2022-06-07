import inject
from fastapi import APIRouter, Depends
from fastapi.encoders import jsonable_encoder

from domain.model.user import User
from domain.ports.database_port import DatabasePort
from domain.services.authentication_service import IAuthenticationService
from domain.exceptions.entity_exceptions import ModelExceptions


@inject.autoparams()
def create_model_router(
    authentication_service: IAuthenticationService, database_port: DatabasePort
):
    router: APIRouter = APIRouter(prefix="/v1/models")

    @router.get("/{model_id}")
    def get_model_by_id(
        model_id: str,
        requesting_user: User = Depends(authentication_service.get_current_user),
    ):
        try:
            model = database_port.get_model_by_id(model_id=model_id)
        except:
            raise ModelExceptions.get_id_not_valid_exception()
        if model is None:
            raise ModelExceptions.get_id_not_found_exception()
        return jsonable_encoder(model.dict())

    @router.get("/")
    def get_model_list(
        requesting_user: User = Depends(authentication_service.get_current_user),
    ):
        try:
            model_list = database_port.get_model_list()
            return jsonable_encoder({"models": model_list})
        except:
            raise ModelExceptions.get_list_exception()

    return router
