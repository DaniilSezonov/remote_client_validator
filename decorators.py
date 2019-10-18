from rest_framework.exceptions import PermissionDenied

_consumers = []


def client_application_required(func, **kwargs):
    _consumers.append(func)

    def wrapper(request):
        if func.__name__ in [consumer.__name__ for consumer in _consumers]:
            # Look at remote_client_validator.middleware
            if not request.client:
                raise PermissionDenied("The client is not allowed.")
            request.client.current_consumer = func.__name__
            return func(request)

    wrapper.__name__ = func.__name__
    return wrapper

