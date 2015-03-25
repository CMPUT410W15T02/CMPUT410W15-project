from django.http import HttpResponse
from django.conf import settings
from django.contrib.auth.models import User

from authors.models import *
from nodes.models import *

import base64

# Modified from https://djangosnippets.org/snippets/1720/
# By schinckel
class APIAuthMiddleware(object):
	def process_request(self, request):
		response = HttpResponse()
		response.status_code = 401
		try:
			realm = settings.HTTP_AUTH_REALM
		except AttributeError:
			realm = ""

		response['WWW-Authenticate'] = 'Basic realm ="%s"' % realm

		if not request.path.startswith('/api/'):
			return

		if 'HTTP_AUTHORIZATION' not in request.META:
			auth = request.META['HTTP_AUTHORIZATION'].split()
		else:
			return response
			
		try:
			uname, host, passwd = base64.b64decode(auth[1]).split(':')
		except:
			return response

		if not Host.objects.filter(url=host).exists():
			return response

		if password != "testpass":
			return response

		try:
			request.user = User.objects.get(username = uname)
		except:
			user = User.objects.create_user(uname, uname+'@'+host, host+'testpass')
			user.is_active = False
			user.save()
			profile = Profile.create_profile(user)
			profile.host = host
			profile.save()
			request.user = user

		return response
		


