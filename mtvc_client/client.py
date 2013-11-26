import hammock


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


class APIClient(object):

    def __init__(self, offering_id, host, port=80, version='v1'):
        self.api = hammock.Hammock(
            'http://%s:%s/api/%s' % (host, port, version),
            append_slash=True)
        self.offering_id = offering_id

    def from_json_response(self, response):
        if response.status_code < 200 or response.status_code >= 300:
            try:
                raise APIClientException(**response.json())
            except APIClientException:
                raise
            except Exception, e:
                raise APIClientException(error_message=str(e))
            except:
                raise APIClientException()

        return response.json()

    def get_channels(self):
        return self.from_json_response(
            self.api.channel.GET(params={'offering': self.offering_id}))[
                'objects']

    def get_shows(self):
        return self.from_json_response(
            self.api.show.GET(params={'offering': self.offering_id}))[
                'objects']

    def get_clips(self):
        return self.from_json_response(
            self.api.clip.GET(params={'offering': self.offering_id}))[
                'objects']

    def get_epg(self, channel_id):
        return self.from_json_response(
            self.api.channel(channel_id).GET(params={'days': 1}))

    def get_stream_url(self, content_type, content_id, user_agent):
        return self.from_json_response(
            self.api(content_type)(content_id).play.GET(
                params={'offering': self.offering_id},
                headers={'User-Agent': user_agent}))

    def get_account_info(self, msisdn):
        return self.from_json_response(self.api.subscriber(msisdn).GET())
