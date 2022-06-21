from pydantic import BaseSettings


class DatabaseSettings(BaseSettings):
    conn_url: str
    database_name: str
    user_collection_name: str
    inference_collection_name: str
    model_collection_name: str
    result_collection_name: str


class AuthenticationSettings(BaseSettings):
    expire_time: str
    key: str
    algorithm: str
