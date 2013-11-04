import hammock


class APIClient(object):

    def __init__(self, offering_id, host, port=80, version='v1'):
        self.api = hammock.Hammock(
            'http://%s:%s/api/%s' % (host, port, version),
            append_slash=True)
        self.offering_id = offering_id

    def get_channels(self):
        return self.api.channel.GET(params={'offering': self.offering_id}).json()['objects']

    def get_shows(self):
        return self.api.show.GET(params={'offering': self.offering_id}).json()['objects']

    def get_clips(self):
        return self.api.clip.GET(params={'offering': self.offering_id}).json()['objects']

    def get_epg(self, channel_id):
        return self.api.channel(channel_id).GET(params={'days': 1}).json()

    def get_stream_url(self, content_type, content_id):
        return self.api(content_type)(content_id).play.GET(
            params={'offering': self.offering_id}).json()

    def get_account_info(self, msisdn):
        return getattr(self.api.subscriber, msisdn).GET().json()

