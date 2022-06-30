from mock import Mock
from nats.aio.client import Client

from adapters.message_service.nats_adapter import NATSAdapter


class NATSMock(NATSAdapter):
    def __init__(self):
        self._conn_url = "fake_url"
        self._nc: Client = Mock(spec=Client)
        self._receiving_nc: Client = Mock(spec=Client)
        self._subs = {}
