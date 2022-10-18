import datetime
import json
from mock import ANY, MagicMock, call, patch
from core.model.constants import Status
from core.model.inference import Inference
from core.model.message_service import RequestLetter
from core.model.result import ResultUpdate
from core.ports.message_service_port import MessageServicePort
from tests.mocks.nats_mock import NATSMock
import pytest
import asyncio

INFERENCE_JSON_1_WITH_ID = {
    "id": "fake_inference_id",
    "gender": "M",
    "age": 23,
    "rgh": "fake_rgh",
    "covid_status": "Sim",
    "mask_type": "None",
    "user_id": "507f191e810c19729de860ea",
    "model_id": "629f994245cda830033cf4cf",
    "status": "processing",
    "cid": "fake_cid",
    "bpm": "fake_bpm",
    "created_in": "2022-07-18 17:07:16.954632",
    "respiratory_frequency": "123",
    "respiratory_insufficiency_status": "Sim",
    "location": "h1",
    "last_positive_diagnose_date": "",
    "hospitalized": "TRUE",
    "hospitalization_start": "2022-07-18 17:07:16.954632",
    "hospitalization_end": "2022-07-18 17:07:16.954632",
    "spo2": "123",
}

adapter_instance = NATSMock()


@pytest.fixture()
def message_service_port():
    port = MessageServicePort(adapter_instance)
    return port


def test_send_message(message_service_port: MessageServicePort):
    async def fake_send_message(topic: str, message: bytes):
        pass

    with patch.object(
        adapter_instance,
        "send_message",
        MagicMock(side_effect=fake_send_message),
    ) as mock_method:
        asyncio.run(
            message_service_port.send_message(
                RequestLetter(
                    content=Inference(**INFERENCE_JSON_1_WITH_ID),
                    publishing_channel="fake_topic",
                ),
            )
        )
        mock_method.assert_called_once_with(
            ANY,
            "fake_topic",
        )


def test_subscribe(message_service_port: MessageServicePort):
    async def fake_subscribe(topic: str):
        pass

    with patch.object(
        adapter_instance,
        "subscribe",
        MagicMock(side_effect=fake_subscribe),
    ) as mock_method:
        asyncio.run(message_service_port.subscribe("fake_topic"))
        mock_method.assert_called_once_with("fake_topic")


def test_wait_for_message(message_service_port: MessageServicePort):
    async def fake_wait_for_message(topic: str):
        return json.dumps(
            {
                "inference_id": "fake_inference_id",
                "output": 0.777,
                "diagnosis": "positive",
            }
        )

    with patch.object(
        adapter_instance,
        "wait_for_message",
        MagicMock(side_effect=fake_wait_for_message),
    ) as mock_method:
        return_value = asyncio.run(message_service_port.wait_for_message("fake_topic"))
        assert return_value == ResultUpdate(
            **{
                "inference_id": "fake_inference_id",
                "output": 0.777,
                "diagnosis": "positive",
            }
        )
