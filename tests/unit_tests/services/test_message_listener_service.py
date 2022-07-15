from mock import MagicMock, patch
import pytest
import asyncio
from core.model.constants import Status
from core.model.result import ResultUpdate
from core.ports.database_port import DatabasePort
from core.ports.message_service_port import MessageServicePort

from core.ports.simple_storage_port import SimpleStoragePort
from tests.mocks.minio_mock import MinioMock
from core.services.message_listener_service import listen_for_messages_and_update
from tests.mocks.mongo_mock import MongoMock
from tests.mocks.nats_mock import NATSMock


@pytest.fixture()
def simple_storage_port():
    port = SimpleStoragePort(MinioMock())
    return port


@pytest.fixture()
def message_service_port():
    port = MessageServicePort(NATSMock())
    return port


@pytest.fixture()
def database_port():
    port = DatabasePort(MongoMock())
    return port


def test_listen_for_messages_and_update(
    database_port: DatabasePort,
    simple_storage_port: SimpleStoragePort,
    message_service_port: MessageServicePort,
):
    async def fake_wait_for_message(central_channel: str):
        return ResultUpdate(
            inference_id="fake_inference_id", output=0.999, diagnosis="positive"
        )

    def fake_remove_inference_directory(inference_id: str):
        pass

    def fake_update_result(result_update: ResultUpdate):
        pass

    def fake_update_inference_status(inference_id: str, status: str):
        pass

    with patch.object(
        message_service_port,
        "wait_for_message",
        MagicMock(side_effect=fake_wait_for_message),
    ) as mock_wait_for_message, patch.object(
        simple_storage_port,
        "remove_inference_directory",
        MagicMock(side_effect=fake_remove_inference_directory),
    ) as mock_remove_inference_directory, patch.object(
        database_port,
        "update_result",
        MagicMock(side_effect=fake_update_result),
    ) as mock_update_result, patch.object(
        database_port,
        "update_inference_status",
        MagicMock(side_effect=fake_update_inference_status),
    ) as mock_update_inference_status:
        asyncio.run(
            listen_for_messages_and_update(
                simple_storage_port,
                message_service_port,
                database_port,
                "fake_central_channel",
            )
        )
        mock_wait_for_message.assert_called_once_with("fake_central_channel")
        mock_update_result.assert_called_once_with(
            ResultUpdate(
                inference_id="fake_inference_id", output=0.999, diagnosis="positive"
            )
        )
        mock_update_inference_status.assert_called_once_with(
            "fake_inference_id", Status.completed_status
        )
        mock_remove_inference_directory.assert_called_once_with("fake_inference_id")
