import base64

from django.http import HttpResponse
from django.template import RequestContext
from django.shortcuts import render_to_response
from django.conf import settings

from mtvc_client.client import APIClientException


class APIClientExceptionMiddleware(object):

    def process_exception(self, request, exception):
        if isinstance(exception, APIClientException):
            if exception.error_code == 'HANDSET_NOT_SUPPORTED':
                return render_to_response(
                    'smart/device_block.html',
                    context_instance=RequestContext(request))

        return None


class BasicAuthMiddleware(object):
    """
    Middleware for HTTP Basic Authentication.

    Requires BASIC_AUTH_CREDS in Django settings which should be a
    dict with passwords keyed by username.
    """

    def get_rfa_response(self):
        response = HttpResponse(
            '<html><title>Authentication required</title><body>'
            '<h1>Authentication Required</h1></body></html>', status=401)
        response['WWW-Authenticate'] = 'Basic realm="Restricted"'
        return response

    def process_request(self, request):
        # fail if we don't have proper BA headers
        try:
            auth_type, data = request.META['HTTP_AUTHORIZATION'].split()
        except KeyError:
            return self.get_rfa_response()

        # this is basic auth only
        if auth_type.lower() != 'basic':
            return self.get_rfa_response()

        # decode the BA data
        try:
            username, password = base64.b64decode(data).decode('utf-8').split(
                ':', 1)
        except (TypeError, ValueError):
            return self.get_rfa_response()

        if not hasattr(settings, 'BASIC_AUTH_CREDS') or \
                settings.BASIC_AUTH_CREDS[username] != password:
            return self.get_rfa_response()

        return None
