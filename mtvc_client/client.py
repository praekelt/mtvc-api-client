import logging

import hammock
from requests.auth import AuthBase


logger = logging.getLogger(__name__)


class APIClientException(Exception):
    """
    Exception class that contains the error code and message from
    the MTVC
    """

    def __init__(self, error_code=None, error_message=None, **kwargs):
        self.error_code = error_code
        self.error_message = error_message

    def __str__(self):
        return '[%(error_code)s] %(error_message)s' % (self.__dict__)


class APIClientAuthentication(AuthBase):
    """
    Attaches Tastypie-style HTTP ApiKey Authentication to the given
    Request object.
    """
    def __init__(self, username, key):
        self.username = username
        self.key = key

    def __call__(self, r):
        r.headers['Authorization'] = 'ApiKey %s:%s' % (self.username, self.key)
        return r


class APIClient(object):

    def __init__(self, offering_id, host, username, key, port=80,
                 version='v1'):
        self.api = hammock.Hammock(
            'http://%s:%s/api/%s' % (host, port, version),
            auth=APIClientAuthentication(username, key),
            append_slash=True)
        self.offering_id = offering_id

    def from_json_response(self, response):
        if response.status_code < 200 or response.status_code >= 300:
            error_context = {
                'status_code': response.status_code,
                'status_reason': response.reason,
                'error_code': response.status_code,
                'error_message': response.reason,
                'content': response.content,
            }

            try:
                error_context.update(response.json())
            except ValueError:
                pass

            logger.error('MTVC Server error %s: %s' % (
                response.status_code, error_context))

            raise APIClientException(**error_context)

        try:
            return response.json()
        except ValueError:
            # the server did not return JSON, so just return {}
            return {}

    def get_countries(self):
        return self.from_json_response(self.api.country.GET())

    def get_channels(self, **kwargs):
        params = {'offering__slug': self.offering_id}
        params.update(kwargs)
        return self.from_json_response(
            self.api.channel.GET(params=params))

    def get_shows(self, **kwargs):
        params = {'offering__slug': self.offering_id}
        params.update(kwargs)
        return self.from_json_response(
            self.api.show.GET(params=params))

    def get_clips(self, **kwargs):
        params = {'offering__slug': self.offering_id}
        params.update(kwargs)
        return self.from_json_response(
            self.api.clip.GET(params=params))

    def get_clip(self, clip_id, **kwargs):
        params = {'offering__slug': self.offering_id}
        params.update(kwargs)
        return self.from_json_response(
            self.api.clip(clip_id).GET(params=params))

    def get_epg(self, channel_id, **kwargs):
        params = {'days': 1}
        params.update(kwargs)
        return self.from_json_response(
            self.api.channel(channel_id).GET(params=params))

    def get_stream_url(
            self, content_type, content_id, user_agent, msisdn, client_ip):
        return self.from_json_response(
            self.api(content_type)(content_id).play.GET(
                params={'offering__slug': self.offering_id},
                headers={
                    'User-Agent': user_agent,
                    'X-MSISDN': msisdn,
                    'X-FORWARDED-FOR': client_ip,
                }))

    def get_account_info(self, msisdn, client_ip):
        return self.from_json_response(self.api.subscriber(msisdn).GET())

    def get_profile_schema(self):
        return self.from_json_response(self.api.subscriberprofile.schema.GET(
            params={'offering__slug': self.offering_id}))

    def post_profile(self, msisdn, client_ip, data):
        return self.from_json_response(self.api.subscriberprofile.POST(
            headers={
                'X-MSISDN': msisdn,
                'X-FORWARDED-FOR': client_ip,
                'Content-Type': 'application/json'},
            params={'offering__slug': self.offering_id},
            data=data))

    def get_transaction_schema(self):
        return self.from_json_response(
            self.api.subscribertransaction.schema.GET(
                params={'offering__slug': self.offering_id}))

    def post_transaction(self, user_agent, msisdn, client_ip, data):
        return self.from_json_response(self.api.subscribertransaction.POST(
            headers={
                'User-Agent': user_agent,
                'X-MSISDN': msisdn,
                'X-FORWARDED-FOR': client_ip,
                'Content-Type': 'application/json'},
            params={'offering__slug': self.offering_id},
            data=data))
