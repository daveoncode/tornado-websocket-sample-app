from __future__ import unicode_literals

from MyApp import MyApp
from tornado.websocket import WebSocketHandler


class HostSocketHandler(WebSocketHandler):
    def __init__(self, application, request, **kwargs):
        super(HostSocketHandler, self).__init__(application, request, **kwargs)
        self.token = request.arguments.get('token', []).pop()
        print 'Received token is: {}'.format(self.token)

    def data_received(self, chunk):
        print 'ClientSocketHandler data_received()'

    def get(self, *args, **kwargs):
        super(HostSocketHandler, self).get(*args, **kwargs)
        print 'adding host with token: {}'.format(self.token)
        MyApp.hosts.add(self)

    def on_message(self, message):
        print 'message received: {}'.format(message)

    def on_close(self):
        MyApp.hosts.remove(self)
        super(HostSocketHandler, self).on_close()
