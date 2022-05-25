from fastapi import FastAPI
import routers.v1.v1 as v1

app = FastAPI()
app.include_router(v1.router)


@app.get("/healthcheck")
def healthcheck():
    return {"message": "OK"}
