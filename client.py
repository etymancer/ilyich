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

	@cachedProperty
	def session(self):
		return requests.session()

	def url(self, *components):
		return urlparse.urljoin(self.ENDPOINT, '/'.join(components))

	def _ensure_token(self):
		if self.token:
			return
		print 'We need a token!'

		params = dict(key=self.key, expiration='never', name=self.NAME,
			    response_type='token', scope='read,write')
		print self.url('authorize')
		request = requests.Request('GET', self.url('authorize'), params=params).prepare()
		print 'Go to {.url} and paste the token here: '.format(request)
		self.token = raw_input()

	def _request(self, method, components, data=None, params=None):
		self._ensure_token()
		url = self.url(*components)
		params = dict(params or {}, key=self.key, token=self.token)
		return self.session.request(method=method, url=url, data=data, params=params)

	def get(self, components, params=None):
		return self._request('GET', components, params=params)

	def post(self, components, params=None):
		return self._request('POST', components, data=params)

	def put(self, components, data=None):
		return self._request('put', components, data=data)

	def delete(self, components):
		return self._request('delete', components)



# 'https://trello.com/1/authorize?key=%s&name=%s&expiration=%s&response_type=token&scope=%s'
# % (self._apikey, quote_plus(app_name), expires, 'read,write' if write_access else 'read')
