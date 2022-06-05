import inject
from fastapi import APIRouter, HTTPException, status
from fastapi.encoders import jsonable_encoder

from domain.dependency_injection.user_actions import UserActions


@inject.autoparams()
def create_user_router(user_actions: UserActions):
    router: APIRouter = APIRouter(prefix="/users")

    @router.get("/{user_id}")
    def get_user_by_id(user_id: str):
        user = user_actions.execute_get_by_id(user_id=user_id)
        if user is None:
            raise HTTPException(status.HTTP_404_NOT_FOUND, "user not found")
        return jsonable_encoder(user.to_dict())

    return router
