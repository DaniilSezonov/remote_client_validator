from django.apps import AppConfig

from backends.remote_client_validator.registred_clients import RegisteredClient, _register


def add_configs_to_register():
    def deep_config_search(cls):
        for sub_cls_config in cls.__subclasses__():
            if not(hasattr(sub_cls_config, "Meta") and sub_cls_config.Meta.only_for_test):
                _register.add(sub_cls_config())
            deep_config_search(sub_cls_config)
    deep_config_search(RegisteredClient)


def clean_client_register():
    _register.clean()


class RemoteClientValidatorConfig(AppConfig):
    name = 'backends.remote_client_validator'

    def ready(self):
        add_configs_to_register()
