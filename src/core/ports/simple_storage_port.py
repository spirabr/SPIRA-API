class SimpleStoragePort:
    def __init__(self, simple_storage_adapter):
        self._simples_storage_adapter = simple_storage_adapter

    def save_file(self, path: str, file) -> None:
        self._simples_storage_adapter.save_file(path, file)
