from fastapi import UploadFile
from mock import MagicMock, patch
import pytest
from core.ports.simple_storage_port import SimpleStoragePort

from tests.mocks.minio_mock import MinioMock

adapter_instance = MinioMock()


@pytest.fixture()
def simple_storage_port():
    port = SimpleStoragePort(adapter_instance)
    return port


def test_store_inference_file(simple_storage_port: SimpleStoragePort):
    def store_inference_file(inference_id, file_type, file) -> None:
        pass

    file = UploadFile("tests/mocks/audio_files/audio1.wav")

    with patch.object(
        adapter_instance,
        "store_inference_file",
        MagicMock(side_effect=store_inference_file),
    ) as mock_store_inference_file:
        simple_storage_port.store_inference_file(
            "507f191e810c19729de860ea",
            "fake_file_type",
            file,
        )

        mock_store_inference_file.assert_called_once_with(
            "507f191e810c19729de860ea",
            "fake_file_type",
            file,
        )


def test_remove_inference_directory(simple_storage_port: SimpleStoragePort):
    def remove_inference_directory(inference_id) -> None:
        pass

    with patch.object(
        adapter_instance,
        "remove_inference_directory",
        MagicMock(side_effect=remove_inference_directory),
    ) as mock_remove_inference_directory:
        simple_storage_port.remove_inference_directory("507f191e810c19729de860ea")

        mock_remove_inference_directory.assert_called_once_with(
            "507f191e810c19729de860ea"
        )
