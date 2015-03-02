from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django.contrib.auth.models import User

from authors.models import Profile

# Register your models here.

class ProfileInline(admin.StackedInline):
	model = Profile

class UserAdmin(UserAdmin):
	inlines = (ProfileInline, )

admin.site.unregister(User)
admin.site.register(User, UserAdmin)
