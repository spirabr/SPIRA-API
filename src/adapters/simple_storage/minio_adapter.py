import os
from minio import Minio


class MinioAdapter:
    def __init__(self, conn_url, access_key, secret_key, bucket_name):
        self._client = Minio(
            conn_url, access_key=access_key, secret_key=secret_key, secure=False
        )
        self._bucket_name = bucket_name
        self._client.make_bucket(bucket_name)

    def store_file(self, inference_id: str, file_type: str, file):
        self._client.put_object(
            self._bucket_name, os.path.join(inference_id, os.sep, file_type), file
        )
