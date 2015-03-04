from django.db import models
from django.contrib.auth.models import User
from authors.models import Profile

# Create your models here.

class Post(models.Model):
    PRIVACY_CHOICES = (('1', 'Public'),
                      ('2', 'Private'),
                      ('3','Custom'),
                      ('4','Friends'))
    post_text = models.TextField(max_length=2048)
    title = models.CharField(max_length=128, blank=True)
    author = models.ForeignKey(Profile) 
    date = models.DateTimeField('date posted')
    privacy = models.CharField(max_length=1, choices=PRIVACY_CHOICES)
    #This will get all the Users for custom do we want that?
    allowed=models.ManyToManyField(User,null=True,blank=True)
   
    def __unicode__(self):
        return str(self.author)

class Comment(models.Model):
    post_id = models.ForeignKey(Post)
    body = models.TextField(max_length=2048)
    author = models.OneToOneField(Profile)
    date = models.DateTimeField('date posted')

    def __unicode__(self):
        return str(self.author)
