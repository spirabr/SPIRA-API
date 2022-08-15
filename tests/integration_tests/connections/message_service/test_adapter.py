import asyncio
import json
from adapters.message_service.nats_adapter import NATSAdapter
import pytest

from src.settings import Settings


@pytest.fixture()
def message_service_adapter():

    adapter = NATSAdapter(
        Settings.message_service_settings.nats_conn_url,
    )
    yield adapter

    # close test remaining connections in case they exist
    if adapter._receiving_nc.is_connected:
        asyncio.run(asyncio.wait_for(adapter._receiving_nc.close(), timeout=5))


@pytest.mark.asyncio
async def test_send_message(message_service_adapter: NATSAdapter):
    try:
        await message_service_adapter.send_message(
            json.dumps(
                {
                    "anything": 123,
                    "model_id": "fake_model_id",
                    "inference_id": "fake_inference_id",
                }
            ),
            "fake_topic",
        )
        assert True
    except:
        assert False


@pytest.mark.asyncio
async def test_subscribe(message_service_adapter: NATSAdapter):
    try:
        await message_service_adapter.subscribe(
            "fake_topic",
        )
        assert True
    except:
        assert False


@pytest.mark.asyncio
async def test_wait_for_message(message_service_adapter: NATSAdapter):
    try:
        await message_service_adapter.subscribe(
            "fake_topic_2",
        )
        await message_service_adapter.send_message(
            json.dumps(
                {
                    "anything": 123,
                    "model_id": "fake_model_id",
                    "inference_id": "fake_inference_id",
                }
            ),
            "fake_topic_2",
        )

        received_message = await message_service_adapter.wait_for_message(
            "fake_topic_2",
        )

        expected_message = json.dumps(
            {
                "anything": 123,
                "model_id": "fake_model_id",
                "inference_id": "fake_inference_id",
            }
        )
        assert received_message == expected_message
    except:
        assert False
