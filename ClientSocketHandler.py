from __future__ import unicode_literals

from tornado.websocket import WebSocketHandler

from MyApp import MyApp


class ClientSocketHandler(WebSocketHandler):
    gestures = ('SWIPE_LEFT', 'SWIPE_RIGHT', 'TAP', 'DOUBLE_TAP')

    def __init__(self, application, request, **kwargs):
        super(ClientSocketHandler, self).__init__(application, request, **kwargs)
        self.token = request.arguments.get('token', []).pop()
        self.host = self.get_host_for_token(self.token)
        print 'ClientSocketHandler - Received token is: {}'.format(self.token)

    def data_received(self, chunk):
        print 'ClientSocketHandler - data_received()'

    @staticmethod
    def get_host_for_token(token):
        for host in MyApp.hosts:
            if host.token == token:
                return host
        return None

    def get(self, *args, **kwargs):
        super(ClientSocketHandler, self).get(*args, **kwargs)
        print 'ClientSocketHandler - get()'
        if self.host:
            print 'sending token back to the [ host ] confirm its validity...'
            self.host.write_message(self.token)
            print 'sending token back to the [ client ] confirm its validity...'
            self.write_message(self.token)
        else:
            print 'closing connection due to invalid token...'
            self.close(401, 'Invalid token ({})'.format(self.token))

    def on_message(self, message):
        print 'ClientSocketHandler - Message received: {}'.format(message)
        if message in self.gestures:
            print 'ClientSocketHandler - Supported gesture... react!'
            self.host.write_message(message)
        else:
            print 'ClientSocketHandler - Unsupported gesture'
