from io import BytesIO
import os

from core.model.inference import UploadAudio


class SimpleStoragePort:
    """Port for the simple storage adapter

    Args:
        simple_storage_adapter (Adapter Class) : simple storage adapter instance

    """

    def __init__(self, simple_storage_adapter):
        self._simples_storage_adapter = simple_storage_adapter

    def store_inference_file(
        self, inference_id: str, file_type: str, audio_file: UploadAudio
    ) -> None:
        """stores the upload_audio in minIO server

        Args:
            inference_id (dict) : inference id
            file_type (str) : type of the file being stored
            audio_file (UploadAudio) : audio file object

        Returns:
            None

        """
        self._simples_storage_adapter.store_inference_file(
            inference_id, file_type, BytesIO(audio_file.content)
        )

    def remove_inference_directory(self, inference_id: str) -> None:
        """removes the inference directory and files from minIO server

        Args:
            inference_id (dict) : inference id

        Returns:
            None

        """
        self._simples_storage_adapter.remove_inference_directory(inference_id)
