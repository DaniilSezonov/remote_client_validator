This is a simple Django app for verification of clients and selecting mail template for it (For example).

Quick start
-----------

1. Add "polls" to your INSTALLED_APPS setting like this::

    INSTALLED_APPS = [
        ...
        'remote-client-validator',
    ]

    MIDDLEWARE = (
      ...
      'backends.remote_client_validator.middleware.ClientValidationMiddleware',
      ...
    )

2. Create clients configs. For example::

  class TestFrontend(RegisteredClient):
      _name = "TestFrontend"
      _host = "http://127.0.0.1:3005"
      _uuid = "7f6s312b-d231-1111-1432-edbeb958b81b"
      _consumer_to_templates_mapping = {
          "forgot_password": "test_fronted/forgot_password.html"
      }
      _default = True


3. Decorate your view "def forgot_password(request)" via @client_application_required decorator.

4. You can access to client and needed template from request variable inside your view like this
 request.client
 request.client.get_template()

