from django.http import HttpResponse

from backends.remote_client_validator import get_client_by_host, get_client_by_uuid
from backends.remote_client_validator.registred_clients import get_default_client


def client_application_required(func, **kwargs):

    bad_request = {
        'status': 400,
        'reason': 'Invalid client'
    }

    def wrapper(request):
        client = None

        app_uuid = request.META.get('HTTP_APPLICATION')

        if app_uuid is None:
            client = get_client_by_host(request.META.get('HTTP_ORIGIN'))
        else:
            client = get_client_by_uuid(app_uuid)

        request.client = client or get_default_client()

        if not request.client:
            return HttpResponse(**bad_request)

        request.client.current_consumer = func.__name__

        return func(request)

    wrapper.__name__ = func.__name__
    return wrapper

