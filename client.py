import os
import requests
import urlparse
from u import cachedProperty

class TrelloClient(object):
    ENDPOINT = 'https://trello.com/1/'
    NAME = 'Dingo Thaw'
    @property
    def key(self):
        return os.environ.get('TRELLO_KEY')

    @property
    def token(self):
        return os.environ.get('TRELLO_TOKEN')

    @token.setter
    def token(self, token):
        os.environ['TRELLO_TOKEN'] = token

    @property
    def token_params(self):
        return dict(key=self.key, expiration='never', name=self.NAME,
                response_type='token', scope='read,write')

    @cachedProperty
    def session(self):
        return requests.session()

    def url(self, *components):
        return urlparse.urljoin(self.ENDPOINT, '/'.join(components))

    def _ensure_token(self):
        if self.token:
            return

        request = requests.Request('GET', self.url('authorize'),
                params=self.token_params).prepare()
        print 'No token set in $TRELLO_TOKEN.'
        print 'Go to {.url} to generate one and paste it here: '.format(request)
        self.token = raw_input()

    def _request(self, method, components, data=None, params=None):
        self._ensure_token()
        url = self.url(*components)
        params = dict(params or {}, key=self.key, token=self.token)
        response = self.session.request(method=method, url=url, data=data, params=params)
        response.raise_for_status()
        return response.json()

    def get(self, components, params=None):
        return self._request('GET', components, params=params)

    def post(self, components, params=None):
        return self._request('POST', components, data=params)

    def put(self, components, data=None):
        return self._request('PUT', components, data=data)

    def delete(self, components):
        return self._request('DELETE', components)



# 'https://trello.com/1/authorize?key=%s&name=%s&expiration=%s&response_type=token&scope=%s'
# % (self._apikey, quote_plus(app_name), expires, 'read,write' if write_access else 'read')
