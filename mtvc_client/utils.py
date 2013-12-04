from django.conf import settings
from django.core.exceptions import ImproperlyConfigured
from django.core.cache import cache

from client import APIClient


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


def get_request_user_agent(request):
    return request.META.get('HTTP_USER_AGENT', '')


def get_profile_schema_cached():
    """
    The API's response for Subscriber Profile schema changes seldomly -
    here we cache the response for 24 hours
    """
    schema = cache.get('profile_schema')
    if not schema:
        schema = APIClient(**settings.API_CLIENT).get_profile_schema()
        cache.set('profile_schema', schema, 60 * 60 * 24)
    return schema


def get_transaction_schema_cached():
    """
    The API's response for Subscriber Transaction schema changes
    seldomly - here we cache the response for 24 hours
    """
    schema = cache.get('transaction_schema')
    if not schema:
        schema = APIClient(**settings.API_CLIENT).get_transaction_schema()
        cache.set('transaction_schema', schema, 60 * 60 * 24)
    return schema


def get_gender_choices():
    schema = get_profile_schema_cached()
    return [['', '---------']] + schema['fields']['gender']['choices']


def get_region_choices():
    schema = get_profile_schema_cached()
    return [['', '---------']] + schema['fields']['region']['choices']


def get_product_choices():
    schema = get_transaction_schema_cached()
    return schema['fields']['product_name']['choices']
