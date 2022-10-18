from mock import MagicMock, patch, call
import pytest
from core.model.inference import InferenceFiles, UploadAudio
from core.ports.simple_storage_port import SimpleStoragePort
from core.services.inference_service import _store_files
from tests.mocks.minio_mock import MinioMock


@pytest.fixture()
def simple_storage_port():
    port = SimpleStoragePort(MinioMock())
    return port


def test_store_files_success(simple_storage_port: SimpleStoragePort):
    def fake_store_inference_file(inference_id, file_type, file) -> None:
        pass

    with patch.object(
        simple_storage_port,
        "store_inference_file",
        MagicMock(side_effect=fake_store_inference_file),
    ) as mock_store_inference_file:

        sustentada = open("tests/mocks/audio_files/audio1.wav", "rb")
        parlenda = open("tests/mocks/audio_files/audio2.wav", "rb")
        frase = open("tests/mocks/audio_files/audio3.wav", "rb")
        aceite = open("tests/mocks/audio_files/audio4.wav", "rb")

        inference_files = InferenceFiles(
            aceite=UploadAudio(content=aceite.read(), filename="aceite.wav"),
            sustentada=UploadAudio(
                content=sustentada.read(), filename="sustentada.wav"
            ),
            parlenda=UploadAudio(content=parlenda.read(), filename="parlenda.wav"),
            frase=UploadAudio(content=frase.read(), filename="frase.wav"),
        )
        _store_files(simple_storage_port, inference_files, "fake_inference_id")
        calls = [
            call(
                "fake_inference_id",
                "aceite",
                inference_files.aceite,
            ),
            call(
                "fake_inference_id",
                "sustentada",
                inference_files.sustentada,
            ),
            call(
                "fake_inference_id",
                "parlenda",
                inference_files.parlenda,
            ),
            call("fake_inference_id", "frase", inference_files.frase),
        ]
        mock_store_inference_file.assert_has_calls(calls)
