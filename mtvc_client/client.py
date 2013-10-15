import requests


class APIClient(object):

    def __init__(self, host, port=80, version='v1'):
        self.root_url = 'http://%s:%s/api/%s' % (host, port, version)

    def _get_response(self, uri, **data):
        params = {'format': 'json'}
        params.update(**data)
        return requests.get('%s%s' % (self.root_url, uri), params=params).json()

    def get_channels(self):
        return self._get_response('/channel/')['objects']

    def get_epg(self, slug):
        return self._get_response('/channel/%s/' % slug, days=1)

    def get_watch(self, slug):
        return self._get_response('/channel/%s/' % slug)

    def get_account_info(self, msisdn):
        return self._get_response('/subscriber/%s/' % msisdn)

