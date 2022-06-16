from fastapi import FastAPI
import uvicorn


from core.ports.database_port import DatabasePort

from adapters.database.mongo import MongoAdapter

from adapters.routers.v1.user_router import create_user_router


def plug_adapters_to_ports():
    ports = {}
    ports["database"] = DatabasePort(MongoAdapter())
    return ports


def create_app(database_port: DatabasePort) -> FastAPI:
    app: FastAPI = FastAPI()
    app.include_router(create_user_router(database_port))
    return app


if __name__ == "__main__":
    ports = plug_adapters_to_ports()
    app = create_app(ports["database"])
    uvicorn.run(
        app,
        host="0.0.0.0",
        port=8000,
        reload=False,
        log_level="debug",
        debug=True,
        workers=1,
    )
