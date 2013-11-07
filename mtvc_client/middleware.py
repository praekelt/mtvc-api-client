from django.template import RequestContext
from django.shortcuts import render_to_response

from mtvc_client.client import APIClientException


class APIClientExceptionMiddleware(object):
    
    def process_exception(self, request, exception):
        if isinstance(exception, APIClientException):
            if exception.error_code == 'HANDSET_NOT_SUPPORTED':
                return render_to_response('smart/device_block.html', context_instance=RequestContext(request))

        return None

