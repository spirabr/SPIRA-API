from mock import ANY, MagicMock, call, patch
from pydantic import BaseModel
from adapters.message_service.nats_adapter import NATSAdapter
from tests.mocks.nats_mock import NATSMock
import pytest
import asyncio


@pytest.fixture()
def message_service_adapter():

    # NATSMock inherits all methods from NATSAdapter
    # but uses a mocked client

    adapter = NATSMock()
    return adapter


def test_send_message(message_service_adapter: NATSAdapter):
    async def fake_publish(topic: str, message: bytes):
        pass

    with patch.object(
        message_service_adapter._nc,
        "publish",
        MagicMock(side_effect=fake_publish),
    ) as mock_method:
        try:
            asyncio.run(
                message_service_adapter.send_message(
                    {
                        "anything": 123,
                        "model_id": "fake_model_id",
                        "inference_id": "fake_inference_id",
                    },
                    "fake_topic",
                )
            )
            assert True
        except:
            assert False
        mock_method.assert_called_once_with(
            "fake_topic",
            str.encode(
                str(
                    {
                        "anything": 123,
                        "model_id": "fake_model_id",
                        "inference_id": "fake_inference_id",
                    }
                ),
                encoding="utf-8",
            ),
        )


def test_subscribe(message_service_adapter: NATSAdapter):
    async def fake_subscribe(topic: str):
        return "return_value_of_subscription"

    with patch.object(
        message_service_adapter._receiving_nc,
        "subscribe",
        MagicMock(side_effect=fake_subscribe),
    ) as mock_method:
        try:
            asyncio.run(
                message_service_adapter.subscribe(
                    "fake_topic",
                )
            )
            assert True
        except:
            assert False

        mock_method.assert_called_once_with("fake_topic")
        assert (
            message_service_adapter._subs["fake_topic"]
            == "return_value_of_subscription"
        )


def test_wait_for_message(message_service_adapter: NATSAdapter):
    async def fake_next_msg():
        class ResponseMock(BaseModel):
            data: bytes

        return ResponseMock(
            data=str.encode("return_value_of_next_msg", encoding="utf-8")
        )

    class SubscriptionMock:
        def __init__(self):
            pass

        async def next_msg(self):
            return "fake_response"

    message_service_adapter._subs["fake_topic"] = SubscriptionMock()
    with patch.object(
        message_service_adapter._subs["fake_topic"],
        "next_msg",
        MagicMock(side_effect=fake_next_msg),
    ) as mock_method:
        try:
            asyncio.run(
                message_service_adapter.wait_for_message(
                    "fake_topic",
                )
            )
            assert True
        except:
            assert False
        mock_method.assert_called_once()
