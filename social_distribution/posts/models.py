from django.db import models
from authors.models import Profile

# Create your models here.

class Post(models.Model):
    post_text = models.TextField(max_length=2048)
    title = models.CharField(max_length=128, blank=True)
    author = models.OneToOneField(Profile)
    date = models.DateTimeField('date posted')
    #Not sure how to handle privacy for privacy to another author
    privacy = models.CharField(max_length=1, blank=True)

    def __unicode__(self):
        return str(self.author)

class Comment(models.Model):
    post_id = models.ForeignKey(Post)
    body = models.TextField(max_length=2048)
    author = models.OneToOneField(Profile)
    date = models.DateTimeField('date posted')

    def __unicode__(self):
        return str(self.author)
