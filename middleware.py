from backends.remote_client_validator.registred_clients import get_client_by_host, get_client_by_uuid, \
    get_default_client


def ClientValidationMiddleware(get_response):
    def middleware(request):
        client = None

        app_uuid = request.META.get('HTTP_Application')

        if app_uuid is None:
            client = get_client_by_host(request.META.get('HTTP_Origin'))
        else:
            client = get_client_by_uuid(app_uuid)

        # If you use django rest framework you can find client there request._request.client
        request.client = client or get_default_client()

        response = get_response(request)
        return response

    return middleware
