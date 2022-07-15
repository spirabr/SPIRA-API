from io import BytesIO
from typing import Iterable
from fastapi import UploadFile
from mock import ANY, MagicMock, patch
from pydantic import BaseModel
import pytest
from adapters.simple_storage.minio_adapter import MinioAdapter
from tests.mocks.minio_mock import MinioMock
from minio.deleteobjects import DeleteObject


@pytest.fixture()
def simple_storage_adapter():
    adapter = MinioMock()
    return adapter


def test_store_inference_file(simple_storage_adapter: MinioAdapter):
    def fake_put_object(bucket_name: str, file_name: str, file: BytesIO, length):
        pass

    with patch.object(
        simple_storage_adapter._client,
        "put_object",
        MagicMock(side_effect=fake_put_object),
    ) as mock_method:
        file = UploadFile("tests/mocks/audio_files/audio1.wav")
        try:
            simple_storage_adapter.store_inference_file(
                "fake_inference_id",
                "fake_file_type",
                file,
            )
            assert True
        except:
            assert False
        mock_method.assert_called_once_with(
            "mock-bucket",
            "fake_inference_id/fake_file_type.wav",
            ANY,
            0,
        )


def test_remove_inference_directory(simple_storage_adapter: MinioAdapter):
    def fake_list_objects(bucket_name: str, inference_id: str, recursive=True):
        class MockObject(BaseModel):
            object_name: str

        return [
            MockObject(object_name="fake_object_1"),
            MockObject(object_name="fake_object_2"),
        ]

    def fake_remove_objects(bucket_name: str, list: Iterable):
        return []

    with patch.object(
        simple_storage_adapter._client,
        "list_objects",
        MagicMock(side_effect=fake_list_objects),
    ) as mock_list_method, patch.object(
        simple_storage_adapter._client,
        "remove_objects",
        MagicMock(side_effect=fake_remove_objects),
    ) as mock_remove_method:
        try:
            simple_storage_adapter.remove_inference_directory("fake_inference_id")
            assert True
        except:
            assert False
        mock_list_method.assert_called_once_with(
            "mock-bucket", "fake_inference_id", recursive=True
        )
        mock_remove_method.assert_called_once_with(
            "mock-bucket",
            ANY,
        )
