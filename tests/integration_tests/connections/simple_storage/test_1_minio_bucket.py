from io import BytesIO
import os
from settings import Settings
from minio import Minio
from minio.deleteobjects import DeleteObject
import pytest


@pytest.fixture()
def client():

    minio_client = Minio(
        Settings.simple_storage_settings.minio_conn_url,
        access_key=Settings.simple_storage_settings.minio_access_key,
        secret_key=Settings.simple_storage_settings.minio_secret_key,
        secure=False,
    )

    if minio_client.bucket_exists("test-bucket"):
        delete_object_list = map(
            lambda x: DeleteObject(x.object_name),
            minio_client.list_objects("test-bucket", recursive=True),
        )
        errors = minio_client.remove_objects("test-bucket", delete_object_list)
        for error in errors:
            print("error occured when deleting object", error, flush=True)
        minio_client.remove_bucket("test-bucket")

    yield minio_client

    if minio_client.bucket_exists("test-bucket"):
        delete_object_list = map(
            lambda x: DeleteObject(x.object_name),
            minio_client.list_objects("test-bucket", recursive=True),
        )
        errors = minio_client.remove_objects("test-bucket", delete_object_list)
        for error in errors:
            print("error occured when deleting object", error, flush=True)
        minio_client.remove_bucket("test-bucket")


def test_bucket_creation(client: Minio):
    client.make_bucket("test-bucket")
    assert client.bucket_exists("test-bucket")


def test_bucket_insert_object(client: Minio):
    client.make_bucket("test-bucket")
    raw_file = BytesIO(open("tests/mocks/audio_files/audio1.wav", "rb").read())
    length = raw_file.getbuffer().nbytes
    client.put_object(
        "test-bucket",
        "fake_inference_id" + os.sep + "fake_file_type" + ".wav",
        raw_file,
        length,
    )

    response = client.get_object(
        "test-bucket",
        "fake_inference_id" + os.sep + "fake_file_type" + ".wav",
    )

    assert response != None
    assert response.data == raw_file.getvalue()
    response.close()
    response.release_conn()
