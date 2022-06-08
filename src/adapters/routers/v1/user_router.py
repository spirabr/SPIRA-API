from fastapi import APIRouter, HTTPException, status
from fastapi.encoders import jsonable_encoder

from core.ports.database_port import DatabasePort
from core.use_cases.user_commands import get_user_by_id_command
from core.model.exception import LogicException


def create_user_router(database_port: DatabasePort):
    router: APIRouter = APIRouter(prefix="/v1/users")

    @router.get("/{user_id}")
    def get_user_by_id(user_id: str):
        command_response = get_user_by_id_command(database_port, user_id)
        if type(command_response) is LogicException:
            raise HTTPException(command_response.error_status, command_response.message)
        return jsonable_encoder(command_response.dict())

    return router
