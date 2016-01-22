import os
import requests
import urlparse
from u import cachedProperty

class TrelloClient(object):
    ENDPOINT = 'https://trello.com/1/'
    NAME = 'Dingo Thaw'
    KEY_NAME = 'TRELLO_KEY'
    TOKEN_NAME = 'TRELLO_TOKEN'

    @property
    def key(self):
        return os.environ[self.KEY_NAME]

    @key.setter
    def key(self, key):
        os.environ[self.KEY_NAME] = key

    @property
    def token(self):
        if self.TOKEN_NAME not in os.environ:
            request = requests.Request('GET', self.url('authorize'),
                    params=self.token_params).prepare()
            print 'No token set in ${}.'.format(self.TOKEN_NAME)
            print 'Go to {.url} to generate one and paste it here: '.format(request)
            self.token = raw_input()
        return os.environ[self.TOKEN_NAME]

    @token.setter
    def token(self, token):
        os.environ[self.TOKEN_NAME] = token

    @property
    def params(self):
        return dict(key=self.key, token=self.token)

    @property
    def token_params(self):
        return dict(key=self.key, expiration='never', name=self.NAME,
                response_type='token', scope='read,write')

    @cachedProperty
    def session(self):
        return requests.session()

    def url(self, *components):
        return urlparse.urljoin(self.ENDPOINT, '/'.join(components))

    def _request(self, method, components, data=None, params={}):
        response = self.session.request(method=method,
                                        url=self.url(*components),
                                        data=data,
                                        params=dict(self.params, **params))
        response.raise_for_status()
        return response.json()

    def get(self, components, params=None):
        return self._request('GET', components, params=params)

    def post(self, components, data=None):
        return self._request('POST', components, data=data)

    def put(self, components, data=None):
        return self._request('PUT', components, data=data)

    def delete(self, components):
        return self._request('DELETE', components)


if __name__ == '__main__':
    client = TrelloClient()
    import IPython;IPython.embed()
