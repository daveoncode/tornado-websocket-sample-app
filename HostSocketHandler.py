from __future__ import unicode_literals

from MyApp import MyApp
from tornado.websocket import WebSocketHandler


class HostSocketHandler(WebSocketHandler):
    def __init__(self, application, request, **kwargs):
        super(HostSocketHandler, self).__init__(application, request, **kwargs)
        self.token = request.arguments.get('token', []).pop()
        print 'HostSocketHandler - Received token is: {}'.format(self.token)

    def data_received(self, chunk):
        print 'HostSocketHandler - data_received()'

    def get(self, *args, **kwargs):
        super(HostSocketHandler, self).get(*args, **kwargs)
        print 'HostSocketHandler - Adding host with token: {}'.format(self.token)
        MyApp.hosts.add(self)

    def on_message(self, message):
        print 'HostSocketHandler - Message received: {}'.format(message)

    def on_close(self):
        print 'HostSocketHandler - Connection closed: removing host "{}"'.format(self.token)
        MyApp.hosts.remove(self)
        super(HostSocketHandler, self).on_close()
