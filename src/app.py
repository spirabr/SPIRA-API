from fastapi import FastAPI
from fastapi.security import OAuth2PasswordBearer
import uvicorn

from pydantic import BaseSettings

from adapters.authentication.authentication_adapter import AuthenticationAdapter
from adapters.database.mongo_adapter import MongoAdapter
from adapters.routers.v1.result_router import create_result_router

from core.ports.authentication_port import AuthenticationPort
from core.ports.database_port import DatabasePort

from adapters.routers.v1.inference_router import create_inference_router
from adapters.routers.v1.model_router import create_model_router
from adapters.routers.v1.user_router import create_user_router

from settings import DatabaseSettings, AuthenticationSettings


def configure_ports():
    database_settings = DatabaseSettings(
        _env_file="database.env", _env_file_encoding="utf-8"
    )
    authentication_settings = AuthenticationSettings(
        _env_file="authentication.env", _env_file_encoding="utf-8"
    )

    ports = {}
    ports["database_port"] = DatabasePort(
        MongoAdapter(
            database_settings.conn_url,
            database_settings.database_name,
            database_settings.user_collection_name,
            database_settings.inference_collection_name,
            database_settings.model_collection_name,
            database_settings.result_collection_name,
        )
    )
    ports["authentication_port"] = AuthenticationPort(
        AuthenticationAdapter(
            authentication_settings.expire_time,
            authentication_settings.key,
            authentication_settings.algorithm,
        )
    )
    return ports


def create_app(ports: dict) -> FastAPI:
    app: FastAPI = FastAPI()

    oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")

    app.include_router(
        create_inference_router(
            ports["authentication_port"], ports["database_port"], oauth2_scheme
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
