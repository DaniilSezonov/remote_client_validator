from django.apps import AppConfig

from backends.remote_client_validator.registred_clients import RegisteredClient, _register


def add_configs_to_register():
    def deep_config_search(cls):
        for sub_cls_config in cls.__subclasses__():
            _register.add(sub_cls_config())
            deep_config_search(sub_cls_config)
    deep_config_search(RegisteredClient)


class RemoteClientValidatorConfig(AppConfig):
    name = 'backends.remote_client_validator'

    def ready(self):
        add_configs_to_register()
