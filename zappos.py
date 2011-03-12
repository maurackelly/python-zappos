import json
import string
import urllib
import urllib2


class ZapposApiException(Exception):
    """
    Zappos exception
    """
    pass


class ZapposApi(object):
    """
    Python bindings for the Zappos API.
    """

    BASE_URL = 'http://api.zappos.com/'

    def __init__(self, api_key):
        """ Must have key. """
        self.api_key = api_key

    def _request(self, path, data={}):
        """ Just grab the response and json it. """
        data['key'] = self.api_key
        url = '%s%s?%s' % (self.BASE_URL, path, urllib.urlencode(data))
        response = urllib.urlopen(url)
        return json.load(response)

    def _camel_case(self, value):
        """ For the awesome urls """
        return string.capwords(value.replace('_', ' ')).replace(' ','')

    def __getattr__(self, name):
        """ Voodoo """
        method = self._camel_case(name)

        def handler(**kwargs):
            return self._request(method, kwargs)

        handler.method = method
        return handler


def main():
    from config import ZAPPOS_KEY
    api = ZapposApi(ZAPPOS_KEY)
    print api.product(id=7718435)
    print api.brand(id=1425)


if __name__ == '__main__':
    main()
