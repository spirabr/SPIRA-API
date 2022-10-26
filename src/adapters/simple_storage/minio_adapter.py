from io import BytesIO
import os
from minio import Minio
from minio.deleteobjects import DeleteObject


class MinioAdapter:
    """Adapter for the minIO server

    Args:
        minio_conn_url (str) : connection url to minIO server container
        bucket_name (str) : name of the bucket used by the app
        minio_access_key (str) : minio access credentials
        minio_secret_key (str) : minio credentials

    """

    def __init__(
        self,
        conn_url: str,
        access_key: str,
        secret_key: str,
        bucket_name: str,
        file_extension: str,
    ):
        self._client = Minio(
            conn_url, access_key=access_key, secret_key=secret_key, secure=False
        )
        self._file_extension = file_extension
        self._bucket_name = bucket_name
        if not self._client.bucket_exists(bucket_name):
            self._client.make_bucket(bucket_name)

    def store_inference_file(
        self, inference_id: str, file_type: str, raw_file: BytesIO
    ):
        """stores the file in minIO server

        Args:
            inference_id (dict) : inference id
            file_type (str) : type of the file being stored
            file_extension (dict) : file extension
            raw_file (BytesIO) : file stream

        Returns:
            None

        """
        length = raw_file.getbuffer().nbytes
        self._client.put_object(
            self._bucket_name,
            inference_id + os.sep + file_type + self._file_extension,
            raw_file,
            length,
        )

    def remove_inference_directory(self, inference_id: str):
        """removes the inference directory and files from minIO server

        Args:
            inference_id (dict) : inference id

        Returns:
            None

        """
        delete_object_list = map(
            lambda x: DeleteObject(x.object_name),
            self._client.list_objects(self._bucket_name, inference_id, recursive=True),
        )
        errors = self._client.remove_objects(self._bucket_name, delete_object_list)
        for error in errors:
            print("error occured when deleting object", error, flush=True)
