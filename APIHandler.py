from __future__ import unicode_literals
from tornado.web import RequestHandler
import json

from flickrapi.core import FlickrAPI


class APIHandler(RequestHandler):
    flickr = FlickrAPI('6840c3f050312de17ff531e20767a597', '89400ed5c8bfb09a', format='json')

    def data_received(self, chunk):
        print 'data received by {}: {}'.format(self.__class__.__name__, chunk)

    @staticmethod
    def format_url(photo, size='b'):
        schema = 'https://farm{farm}.staticflickr.com/{server}/{id}_{secret}_{size}.jpg'
        return schema.format(farm=photo['farm'],
                             server=photo['server'],
                             id=photo['id'],
                             secret=photo['secret'],
                             size=size)

    def get_flickr_images(self):
        print 'calling flickr API...'
        response = self.flickr.photos.search(privacy_filter=1,
                                             min_upload_date='2012-01-01',
                                             safe_search=1,
                                             content_type=1,
                                             tags='landscape')
        data = json.loads(response)
        urls = [{'large': self.format_url(p), 'thumb': self.format_url(p, 'q')} for p in data['photos']['photo'][:12]]
        return json.dumps(urls)

    def get(self, *args, **kwargs):
        print 'incoming request handled by {}'.format(self.__class__.__name__)
        self.write(self.get_flickr_images())

    def write_error(self, status_code, **kwargs):
        print 'write_error()'
        self.write('Ops... something went wrong :/')
