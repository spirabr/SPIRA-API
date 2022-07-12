class SimpleStoragePort:
    def __init__(self, simple_storage_adapter):
        self._simples_storage_adapter = simple_storage_adapter

    def store_file(self, inference_id: str, file_type: str, file) -> None:
        self._simples_storage_adapter.save_file(inference_id, file_type, file)
