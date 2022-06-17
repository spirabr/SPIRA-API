from fastapi import APIRouter, HTTPException, Request, status
from fastapi.encoders import jsonable_encoder
from adapters.routers.v1.utils.auth import get_header_bearer_token
from core.model.exception import LogicException
from core.model.token import Token

from core.ports.authentication_port import AuthenticationPort
from core.ports.database_port import DatabasePort
from core.services.result_service import get_inference_result


def create_result_router(
    authentication_port: AuthenticationPort, database_port: DatabasePort
):
    router: APIRouter = APIRouter(prefix="/v1/users")

    @router.get("/{user_id}/inferences/{inference_id}/result")
    def get_result(inference_id: str, user_id: str, req: Request):
        try:
            token_content = get_header_bearer_token(req)
        except:
            raise HTTPException(status.HTTP_401_UNAUTHORIZED, "Not authenticated")

        try:
            inference, result = get_inference_result(
                authentication_port,
                database_port,
                inference_id,
                user_id,
                Token(content=token_content),
            )
        except LogicException as e:
            raise HTTPException(e.error_status, e.message)

        return jsonable_encoder(
            {"inference": inference.dict(), "result": result.dict()}
        )

    return router
