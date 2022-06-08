from fastapi import APIRouter, HTTPException, status
from fastapi.encoders import jsonable_encoder

from domain.ports.database_port import DatabasePort


def create_user_router(database_port: DatabasePort):
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

    return router
