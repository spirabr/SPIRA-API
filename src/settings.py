from pydantic import BaseSettings


class DatabaseSettings(BaseSettings):
    mongo_conn_url: str
    database_name: str
    user_collection_name: str
    inference_collection_name: str
    model_collection_name: str
    result_collection_name: str


class AuthenticationSettings(BaseSettings):
    expire_time: int
    key: str
    algorithm: str
    context_scheme: str
    deprecated: str


class MessageServiceSettings(BaseSettings):
    nats_conn_url: str


class MessageListenerSettings(BaseSettings):
    loop_timeout: int
    loop_interval: int
    central_channel: str


class SimpleStorageSettings(BaseSettings):
    simple_storage_conn_url: str
    bucket_name: str


class Settings:

    database_settings = DatabaseSettings(
        _env_file="database.env", _env_file_encoding="utf-8"
    )

    authentication_settings = AuthenticationSettings(
        _env_file="authentication.env", _env_file_encoding="utf-8"
    )

    message_service_settings = MessageServiceSettings(
        _env_file="message_service.env", _env_file_encoding="utf-8"
    )

    message_listener_settings = MessageListenerSettings(
        _env_file="message_listener.env", _env_file_encoding="utf-8"
    )

    simple_storage_settings = SimpleStorageSettings(
        _env_file="simple_storage.env", _env_file_encoding="utf-8"
    )
