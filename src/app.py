from fastapi import FastAPI
import uvicorn

from configuration import inject_dependencies
from routers.v1.user_router import create_user_router
from routers.v1.inference_router import create_inference_router


def create_app() -> FastAPI:
    app: FastAPI = FastAPI()
    app.include_router(create_user_router())
    app.include_router(create_inference_router())
    return app


if __name__ == "__main__":
    inject_dependencies()
    uvicorn.run(
        create_app(),
        host="0.0.0.0",
        port=8000,
        reload=False,
        log_level="debug",
        debug=True,
        workers=1,
    )
