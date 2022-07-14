from fastapi import UploadFile


class SimpleStoragePort:
    def __init__(self, simple_storage_adapter):
        self._simples_storage_adapter = simple_storage_adapter

    def store_file(self, inference_id: str, file_type: str, file: UploadFile) -> None:
        self._simples_storage_adapter.store_file(inference_id, file_type, file)
