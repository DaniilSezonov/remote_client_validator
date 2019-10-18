import json

from django.test import RequestFactory, TestCase

from backends.remote_client_validator.apps import add_configs_to_register
from .registred_clients import _register, _OnlyForTestClient
from .decorators import client_application_required


@client_application_required
def tested_view(request):
    from django.http import JsonResponse
    return JsonResponse({'client': request.client.name})


class RemoteClientValidatorTests(TestCase):
    view_path = '/test/'

    request_factory = RequestFactory()

    class TestApplication(_OnlyForTestClient):
        _name = "TestApplication"
        _host = "http://127.0.0.1:3005"
        _uuid = "11111111-1111-1111-1111-111111111111"

    class DefaultApplication(TestApplication):
        _name = "Default application"
        _host = ""
        _uuid = ""
        _default = True

    @classmethod
    def setUpClass(cls):
        # удаляем все реально зарегистрированные клиенты перед каждым тестом. В том числе и дефолтный.
        _register.clean()
        _register.add(cls.TestApplication())
        _register.add(cls.DefaultApplication())

    def test_default_application(self):
        request = self.request_factory.post(path=self.view_path)
        response = tested_view(request)
        data = json.loads(response.getvalue())
        self.assertEqual(data.get('client'), self.DefaultApplication().name)

    def test_client_validation_by_uuid(self):
        request = self.request_factory.post(path=self.view_path, **{"HTTP_APPLICATION": self.TestApplication().uuid})
        response = tested_view(request)
        data = json.loads(response.getvalue())
        self.assertEqual(data.get('client'), self.TestApplication().name)

    def test_client_validation_by_host(self):
        request = self.request_factory.post(path=self.view_path, **{"HTTP_ORIGIN": self.TestApplication().host})
        response = tested_view(request)
        data = json.loads(response.getvalue())
        self.assertEqual(data.get('client'), self.TestApplication().name)

    def test_validation_error_if_default_client_is_not_set(self):
        _register._register = []
        _register._default = None
        _register.add(self.TestApplication())

        request = self.request_factory.post(path=self.view_path)
        response = tested_view(request)
        self.assertEqual(response.status_code, 400)

    @classmethod
    def tearDownClass(cls):
        _register.clean()
        # возвращаем реальные конфиги
        add_configs_to_register()
