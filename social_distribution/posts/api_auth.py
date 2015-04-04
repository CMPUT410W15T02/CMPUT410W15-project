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

		if not request.path.startswith('/api/'):
			return

		if 'HTTP_AUTHORIZATION' in request.META:
			auth = request.META['HTTP_AUTHORIZATION'].split()
		else:
			return make_response("Not Authenticated!")

		try:
			uname, passwd = base64.b64decode(auth[1]).split(':')
		except:
			return make_response("HTTP Auth Error!")

		if Host.objects.filter(password=passwd).exists():
			host_obj = Host.objects.get(password=passwd)
		else:
			return make_response("HTTP Auth Error!")
        
		if host_obj.share == False:
			return make_response("Connection Refused")    

		try:
			request.user = User.objects.get(username = uname+':'+host_obj.name)
		except:
			user = User.objects.create_user(uname+':'+host_obj.name, uname+'@'+host_obj.host_url, host_obj.name)
			user.is_active = False
			user.save()
			profile = Profile.create_profile(user)
			profile.host = host_obj.host_url
			profile.save()
			request.user = user

def make_response(message):
	response = HttpResponse()
	response.status_code = 401
	try:
		realm = settings.HTTP_AUTH_REALM
	except AttributeError:
		realm = ""
	response['WWW-Authenticate'] = 'Basic realm ="%s"' % realm
	response['Message'] = message
	return response
