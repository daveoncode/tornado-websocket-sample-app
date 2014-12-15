from __future__ import unicode_literals
from APIHandler import APIHandler

from ClientSocketHandler import ClientSocketHandler
from HomePageHandler import HomePageHandler
from HostSocketHandler import HostSocketHandler
from MyApp import MyApp
from tornado.ioloop import IOLoop
from tornado.web import StaticFileHandler
import os


def main():
    print 'setting up tornado...'
    handlers = [
        (r'/', HomePageHandler),
        (r'/ws/host/', HostSocketHandler),
        (r'/ws/client/', ClientSocketHandler),
        (r'/static/(.*)', StaticFileHandler),
        (r'/api/', APIHandler)
    ]
    settings = dict(static_path=os.path.join(os.path.dirname(__file__), 'static'))
    app = MyApp(handlers, **settings)
    app.listen(5000)
    IOLoop.instance().start()


if __name__ == '__main__':
    main()
