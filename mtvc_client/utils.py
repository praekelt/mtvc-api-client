from django.conf import settings
from django.core.exceptions import ImproperlyConfigured


def get_request_msisdn(request):
    try:
        return request.META.get(settings.MSISDN_HEADER, '')
    except AttributeError:
        raise ImproperlyConfigured(
            'Missing setting MSISDN_HEADER in the settings file')


def get_request_ip(request):
    try:
        return request.META.get(settings.CLIENT_IP_HEADER, '')
    except AttributeError:
        raise ImproperlyConfigured(
            'Missing setting CLIENT_IP_HEADER in the settings file')
