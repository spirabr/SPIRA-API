from adapters.message_service.nats_adapter import NATSAdapter
from tests.mocks.nats_mock import NATSMock
import pytest
from nats.aio.client import Client


@pytest.fixture()
def message_service_adapter():

    # NATSMock inherits all methods from NATSAdapter
    # but uses a mocked client

    adapter = NATSMock()
    return adapter


async def test_send_message(message_service_adapter: NATSAdapter):
    pass


async def test_subscribe(message_service_adapter: NATSAdapter):
    pass


async def test_wait_for_message(message_service_adapter: NATSAdapter):
    pass
