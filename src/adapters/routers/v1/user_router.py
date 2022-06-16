from fastapi import APIRouter, HTTPException, status
from fastapi.encoders import jsonable_encoder

from core.ports.database_port import DatabasePort
from core.services.user_service import get_by_id
from core.model.exception import LogicException


def create_user_router(database_port: DatabasePort):
    router: APIRouter = APIRouter(prefix="/v1/users")

    @router.get("/{user_id}")
    def get_user_by_id(user_id: str):
        try:
            command_response = get_by_id(database_port, user_id)
        except LogicException as e:
            raise HTTPException(e.error_status, e.message)
        return jsonable_encoder(command_response.dict())

    return router
