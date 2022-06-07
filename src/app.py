from fastapi import FastAPI
import uvicorn

from routers.v1.user_router import create_user_router

from domain.ports.database_port import DatabasePort

from adapters.database.mongo import MongoAdapter


def create_app() -> FastAPI:
    app: FastAPI = FastAPI()
    database_port = DatabasePort(MongoAdapter())
    app.include_router(create_user_router(database_port))
    return app


if __name__ == "__main__":
    uvicorn.run(
        create_app(),
        host="0.0.0.0",
        port=8000,
        reload=False,
        log_level="debug",
        debug=True,
        workers=1,
    )
