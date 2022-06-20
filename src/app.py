from fastapi import FastAPI
from fastapi.security import OAuth2PasswordBearer
import uvicorn


from adapters.authentication.authentication_adapter import AuthenticationAdapter
from adapters.database.mongo_adapter import MongoAdapter
from adapters.message_service.nats_adapter import NATSAdapter

from core.ports.authentication_port import AuthenticationPort
from core.ports.database_port import DatabasePort
from core.ports.message_service_port import MessageServicePort

from adapters.routers.v1.result_router import create_result_router
from adapters.routers.v1.inference_router import create_inference_router
from adapters.routers.v1.model_router import create_model_router
from adapters.routers.v1.user_router import create_user_router


def configure_ports():
    ports = {}
    ports["database_port"] = DatabasePort(MongoAdapter())
    ports["authentication_port"] = AuthenticationPort(AuthenticationAdapter())
    ports["message_service_port"] = MessageServicePort(NATSAdapter.create_adapter())
    return ports


def create_app(ports: dict) -> FastAPI:
    app: FastAPI = FastAPI()

    oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")

    app.include_router(
        create_inference_router(
            ports["message_service_port"],
            ports["authentication_port"],
            ports["database_port"],
            oauth2_scheme,
        )
    )
    app.include_router(
        create_model_router(
            ports["authentication_port"], ports["database_port"], oauth2_scheme
        )
    )
    app.include_router(
        create_user_router(
            ports["authentication_port"], ports["database_port"], oauth2_scheme
        )
    )
    app.include_router(
        create_result_router(
            ports["authentication_port"], ports["database_port"], oauth2_scheme
        )
    )
    return app


if __name__ == "__main__":
    app = create_app(configure_ports())
    uvicorn.run(
        app,
        host="0.0.0.0",
        port=8000,
        reload=False,
        log_level="debug",
        debug=True,
        workers=1,
    )
