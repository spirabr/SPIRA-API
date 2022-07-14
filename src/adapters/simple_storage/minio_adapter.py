import os
import io
from fastapi import UploadFile
from minio import Minio


class MinioAdapter:
    def __init__(self, conn_url, access_key, secret_key, bucket_name):
        self._client = Minio(
            conn_url, access_key=access_key, secret_key=secret_key, secure=False
        )
        self._bucket_name = bucket_name
        if not self._client.bucket_exists(bucket_name):
            self._client.make_bucket(bucket_name)

    def store_file(self, inference_id: str, file_type: str, file: UploadFile):
        raw_file = io.BytesIO(file.file.read())
        length = raw_file.getbuffer().nbytes
        _, file_extension = os.path.splitext(file.filename)
        self._client.put_object(
            self._bucket_name,
            inference_id + os.sep + file_type + file_extension,
            raw_file,
            length,
        )
