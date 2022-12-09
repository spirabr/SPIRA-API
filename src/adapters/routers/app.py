from adapters.routers.v1.hospital_router import create_hospital_router
from fastapi import FastAPI
from fastapi.security import OAuth2PasswordBearer
import uvicorn
from fastapi.middleware.cors import CORSMiddleware
import os

from adapters.routers.v1.result_router import create_result_router
from adapters.routers.v1.inference_router import create_inference_router
from adapters.routers.v1.model_router import create_model_router
from adapters.routers.v1.user_router import create_user_router
from core.ports.ports import Ports


def create_app(ports: Ports) -> FastAPI:
    app: FastAPI = FastAPI()

    app.add_middleware(
        CORSMiddleware,
        allow_origins=[
            os.environ['CLIENT_URL'],
        ],
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )

    oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")

    app.include_router(
        create_inference_router(
            ports.simple_storage_port,
            ports.message_service_port,
            ports.authentication_port,
            ports.database_port,
            oauth2_scheme,
        )
    )
    app.include_router(
        create_model_router(
            ports.authentication_port, ports.database_port, oauth2_scheme
        )
    )
    app.include_router(
        create_user_router(
            ports.authentication_port, ports.database_port, oauth2_scheme
        )
    )
    app.include_router(
        create_result_router(
            ports.authentication_port, ports.database_port, oauth2_scheme
        )
    )
    app.include_router(
        create_hospital_router(
            ports.authentication_port, ports.database_port, oauth2_scheme
        )
    )
    return app


def run_app(ports: dict):
    app = create_app(ports)
    uvicorn.run(
        app,
        host="0.0.0.0",
        port=8000,
        reload=False,
        log_level="debug",
        debug=True,
        workers=1,
    )
