from adapters.simple_storage.minio_adapter import MinioAdapter
from minio import Minio
from mock import Mock


class MinioMock(MinioAdapter):
    def __init__(self):
        self._client: Minio = Mock(spec=Minio)
        self._bucket_name = "mock-bucket"
        self._client.make_bucket(self._bucket_name)
