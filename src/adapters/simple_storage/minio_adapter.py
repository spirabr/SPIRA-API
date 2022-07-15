from io import BytesIO
import os
from minio import Minio
from minio.deleteobjects import DeleteObject


class MinioAdapter:
    def __init__(self, conn_url, access_key, secret_key, bucket_name):
        self._client = Minio(
            conn_url, access_key=access_key, secret_key=secret_key, secure=False
        )
        self._bucket_name = bucket_name
        if not self._client.bucket_exists(bucket_name):
            self._client.make_bucket(bucket_name)

    def store_inference_file(
        self, inference_id: str, file_type: str, file_extension: str, raw_file: BytesIO
    ):

        length = raw_file.getbuffer().nbytes
        self._client.put_object(
            self._bucket_name,
            inference_id + os.sep + file_type + file_extension,
            raw_file,
            length,
        )

    def remove_inference_directory(self, inference_id: str):
        delete_object_list = map(
            lambda x: DeleteObject(x.object_name),
            self._client.list_objects(self._bucket_name, inference_id, recursive=True),
        )
        errors = self._client.remove_objects(self._bucket_name, delete_object_list)
        for error in errors:
            print("error occured when deleting object", error, flush=True)
