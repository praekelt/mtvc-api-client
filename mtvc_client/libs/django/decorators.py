from functools import wraps

from django.core.urlresolvers import reverse
from django.http import HttpResponseRedirect

from mtvc_client.client import APIClientException


def view_exception_handler(view_func):
    """
    A view decorator that undestands MTVC error codes and how to deal
    with the state changes that they hint at.

    Eg when a Subscriber's Profile information is incomplete or outdated
    then the API returns HTTP 401 (Unauthorized) with the following
    error details in the response:
        {
            "error_code": "NO_SUBSCRIBER_PROFILE"
        }

    The API client would catch these, raise APIClientException and add
    the error details to the exception context.
    """

    def _decorator(request, *args, **kwargs):
        try:
            return view_func(request, *args, **kwargs)
        except APIClientException, e:
            if e.error_code == 'HANDSET_NOT_SUPPORTED':
                return HttpResponseRedirect(reverse('handset-not-supported'))

            if e.error_code == 'NO_SUBSCRIBER_PROFILE':
                return HttpResponseRedirect(reverse('profile'))

            if e.error_code == 'NO_SUBSCRIPTION':
                return HttpResponseRedirect(reverse('product'))

            if e.error_code == 'TRANSACTION_FAILED':
                return HttpResponseRedirect(reverse('transaction-failed'))

            raise

    return wraps(view_func)(_decorator)
