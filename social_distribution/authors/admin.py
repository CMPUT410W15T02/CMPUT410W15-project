from django.contrib import admin
from authors.models import Author, Profile

# Register your models here.

class ProfileInLine(admin.StackedInline):
    model = Profile

class AuthorAdmin(admin.ModelAdmin):
    list_display = ('username', 'name')
    inlines = [ProfileInLine]

    def name(self, instance):
        return instance.profile.name

admin.site.register(Author, AuthorAdmin)
