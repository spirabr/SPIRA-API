from pydantic import BaseSettings


class DatabaseSettings(BaseSettings):
    """Settings holding the environment variables for the MongoAdapter

    Attributes:
        mongo_conn_url (str) : connection url to mongoDB container
        database_name (str) : name of the database used
        user_collection_name (str) : name of the collection referring to users
        inference_collection_name (str) : name of the collection referring to inferences
        model_collection_name (str) : name of the collection referring to models
        result_collection_name (str) : : name of the collection referring to results

    """

    mongo_conn_url: str
    database_name: str
    user_collection_name: str
    inference_collection_name: str
    model_collection_name: str
    result_collection_name: str


class AuthenticationSettings(BaseSettings):
    """Settings holding the environment variables for the AuthenticationAdapter

    Attributes:
        expire_time (int) : token expire time
        key (str) : secret key used to generate token
        algorithm (str) : algorithm used to generate token
        context_scheme (str) : encryption context scheme
        deprecated (str) : encryption context parameter

    """

    expire_time: int
    key: str
    algorithm: str
    context_scheme: str
    deprecated: str


class MessageServiceSettings(BaseSettings):
    """Settings holding the environment variables for the NATSAdapter

    Attributes:
        nats_conn_url (str) : connection url to NATS server container

    """

    nats_conn_url: str


class MessageListenerSettings(BaseSettings):
    """Settings holding the environment variables for the message listener process

    Attributes:
        loop_interval (int) : time interval between loop iterations
        central_channel (str) : message service channel used to receive update messages

    """

    loop_interval: int
    central_channel: str


class SimpleStorageSettings(BaseSettings):
    """Settings holding the environment variables for the MinioAdapter

    Attributes:
        minio_conn_url (str) : connection url to minIO server container
        bucket_name (str) : name of the bucket used by the app
        minio_access_key (str) : minio access credentials
        minio_secret_key (str) : minio credentials

    """

    minio_conn_url: str
    bucket_name: str
    minio_access_key: str
    minio_secret_key: str


class Settings:
    """Settings gathering the environment variables for all adapters

    Attributes:
        database_settings (DatabaseSettings) : database settings object
        authentication_settings (AuthenticationSettings) : authentication settings object
        message_service_settings (MessageServiceSettings) : message_service settings object
        message_listener_settings (MessageListenerSettings) : message_listener settings object
        simple_storage_settings (SimpleStorageSettings) : simple_storage settings object

    """

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
