import unittest
import threading
import SocketServer
import BaseHTTPServer

from nose.tools import assert_raises

from mtvc_client.client import APIClient, APIClientException


HOST_NAME = 'localhost'
PORT_NUMBER = 9999

RESP_SUBS_VALIDATION_ERROR = """{
    "subscriberprofile": {
        "subscriber": [
            "Subscriber profile with this Subscriber already exists."
        ]
    },
    "error_message": "Validation error",
    "error_code": "ERROR_VALIDATION"
}"""


class TestHTTPServer(SocketServer.ThreadingMixIn, BaseHTTPServer.HTTPServer):
    pass


class TestHandler(BaseHTTPServer.BaseHTTPRequestHandler):

    def do_GET(s):
        """
        Returns fixed HTTP responses
        """
        s.send_response(400)
        s.send_header("Content-type", "text/json")
        s.end_headers()

        if s.path.lower().startswith('/api/v1/channel/1/play/'):
            s.wfile.write(RESP_SUBS_VALIDATION_ERROR)

    def log_message(self, *args, **kwargs):
        # silencio!
        pass


class TestClient(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        cls.server = TestHTTPServer((HOST_NAME, PORT_NUMBER), TestHandler)
        server_thread = threading.Thread(target=cls.server.serve_forever)
        server_thread.daemon = True
        server_thread.start()

        cls.client = APIClient(
            offering_id='test',
            host='localhost',
            username='test',
            key='test',
            port=9999)

    @classmethod
    def tearDownClass(cls):
        cls.server.shutdown()

    def test_01_subscriber_exists_error(self):
        assert_raises(
            APIClientException,
            self.client.get_stream_url,
            content_type='channel',
            content_id=1,
            user_agent='test',
            msisdn='test',
            client_ip='127.0.0.1',
            )

        try:
            self.client.get_stream_url(
                content_type='channel',
                content_id=1,
                user_agent='test',
                msisdn='test',
                client_ip='127.0.0.1',
            )
        except APIClientException, e:
            assert hasattr(e, 'subscriberprofile')
            assert 'subscriber' in e.subscriberprofile
            assert len(e.subscriberprofile['subscriber']) == 1
            assert e.subscriberprofile['subscriber'][0] == \
                'Subscriber profile with this Subscriber already exists.'
