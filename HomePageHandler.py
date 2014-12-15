from __future__ import unicode_literals
import string
import random

from tornado.web import RequestHandler
from user_agents import parse


class HomePageHandler(RequestHandler):
    def __init__(self, application, request, **kwargs):
        super(HomePageHandler, self).__init__(application, request, **kwargs)
        self.token = self.generate_token()

    @staticmethod
    def generate_token():
        signs = string.ascii_uppercase + string.digits
        return ''.join(random.choice(signs) for _ in range(5))

    def data_received(self, chunk):
        print 'HomePageHandler - Data received by {}: {}'.format(self.__class__.__name__, chunk)

    def get(self, *args, **kwargs):
        print 'HomePageHandler - Incoming request handled by {}'.format(self.__class__.__name__)
        agent = parse(self.request.headers.get('User-Agent', ''))
        is_client = (agent.is_mobile or agent.is_tablet) and agent.is_touch_capable
        self.render('templates/home.html', token=self.token, is_client=is_client, device=agent.device.family)

    def write_error(self, status_code, **kwargs):
        print 'HomePageHandler - write_error()'
        self.write('Ops... something went wrong :/')
