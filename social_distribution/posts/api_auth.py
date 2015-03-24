from django.http import HttpResponse
from django.conf import settings

from authors.models import *
from nodes.models import *

import base64

# Modified from https://djangosnippets.org/snippets/1720/
# By schinckel
class APIAuthMiddleware(object):
	def process_request(self, request):
		if not request.path.startswith('/api/'):
			return

		if request.META.has.key('HTTP_AUTHORIZATION'):
			auth = request.META['HTTP_AUTHORIZATION'].split()
			if len(auth) == 2:
				if auth[0].lower() == 'basic':
					uname, host, passwd = base64.b64decode(auth[1]).split(':')

		response = HttpResponse()
		response.status_code = 401
		try:
			realm = settings.HTTP_AUTH_REALM
		except AttributeError:
			realm = ""

		response['WWW-Authenticate'] = 'Basic realm ="%s"' % realm
		return response
		


