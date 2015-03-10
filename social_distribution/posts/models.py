from django.db import models
from django.contrib.auth.models import User
from authors.models import Profile
import uuid

# Create your models here.

class Post(models.Model):
    uuid = models.CharField(max_length=36, default = uuid.uuid4)
    PRIVACY_CHOICES = (('1', 'Public'),
                      ('2', 'Private'),
                      ('3','Custom'),
                      ('4','Friends'))
    title = models.CharField(max_length=128, blank=True)
    description = models.CharField(max_length=512, blank=True)
    content_type = models.CharField(max_length=16)
    post_text = models.TextField(max_length=2048)
    image = models.ImageField(upload_to='post_images', blank=True)
    author = models.ForeignKey(Profile)
    date = models.DateTimeField('date posted')
    privacy = models.CharField(max_length=1, choices=PRIVACY_CHOICES)
    #This will get all the Users for custom do we want that?
    allowed=models.ManyToManyField(User,null=True,blank=True)
    
    def get_image_name(image):
        return image.url
    def __unicode__(self):
        return str(self.author)

class Comment(models.Model):
    post_id = models.ForeignKey(Post)
    uuid = models.CharField(max_length=36, default = uuid.uuid4)
    body = models.TextField(max_length=2048)
    author = models.ForeignKey(Profile)
    date = models.DateTimeField('date posted')

    def __unicode__(self):
        return str(self.author)
