from typing import List
import logging

logger = logging.getLogger("remote_client_validator")


class RegisteredClientMeta(type):
    def merge_consumer_to_templates_mappings(cls):
        return {**cls._consumer_to_templates_mapping, **cls.__bases__[0]._consumer_to_templates_mapping}


class RegisteredClient(object, metaclass=RegisteredClientMeta):
    _name: str
    _host: str or None
    _uuid: str
    _consumer_to_templates_mapping: dict = {}
    _default: bool = False
    _current_consumer: str or None = None

    @property
    def name(self):
        return self._name

    @property
    def host(self):
        return self._host

    @property
    def uuid(self):
        return self._uuid

    @property
    def default(self):
        return self._default

    def get_template(self, consumer_name=None):
        if consumer_name is None and self.current_consumer:
            try:
                return self._consumer_to_templates_mapping[self.current_consumer]
            except KeyError:
                logger.debug("Failed to find template for that consumer (view).")
                return None
        return self._consumer_to_templates_mapping.get(consumer_name, None)

    @property
    def current_consumer(self):
        return self._current_consumer

    @current_consumer.setter
    def current_consumer(self, value):
        self._current_consumer = value

    def __new__(cls, *args, **kwargs):
        cls._consumer_to_templates_mapping = cls.__class__.merge_consumer_to_templates_mappings(cls)
        return super(RegisteredClient, cls).__new__(cls, *args, **kwargs)


class ClientRegister(object):
    _register: List[RegisteredClient] = []
    _default = None

    def __iter__(self):
        return self._register.__iter__()

    @property
    def default(self):
        return self._default

    def add(self, item: RegisteredClient):
        assert not (self.default and item.default), "Only one client can mark as 'default', " \
                                                          "check your clients config (RegisteredClients inheritors)."
        if item.default:
            self._default = item
        self._register.append(item)


_register: ClientRegister = ClientRegister()


def get_client_by_uuid(uuid: str):
    next((client for client in _register if client.uuid == uuid), None)


def get_client_by_host(host: str):
    next((client for client in _register if client.host == host), None)


def get_default_client():
    return _register.default
