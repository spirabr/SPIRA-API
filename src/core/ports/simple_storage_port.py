from fastapi import UploadFile


class SimpleStoragePort:
    def __init__(self, simple_storage_adapter):
        self._simples_storage_adapter = simple_storage_adapter

    def store_inference_file(
        self, inference_id: str, file_type: str, file: UploadFile
    ) -> None:
        self._simples_storage_adapter.store_inference_file(
            inference_id, file_type, file
        )

    def remove_inference_directory(self, inference_id: str) -> None:
        self._simples_storage_adapter.remove_inference_directory(inference_id)
