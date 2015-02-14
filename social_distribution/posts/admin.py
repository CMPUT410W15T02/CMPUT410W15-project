from django.contrib import admin
from posts.models import Post, Comment

# Register your models here.
class CommentInLine(admin.StackedInline):
    model = Comment

class PostAdmin(admin.ModelAdmin):
    list_display = ('author', 'post_text')
    inlines = [CommentInLine]

admin.site.register(Post, PostAdmin)
