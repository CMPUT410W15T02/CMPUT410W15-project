from django.db import models
from django.contrib.auth.models import User
from authors.models import Profile
import uuid

# Create your models here.

class Post(models.Model):
    PRIVACY_CHOICES = (('1', 'Public'),
                      ('2', 'Private'),
                      ('3','Friend of a Friend'),
                      ('4','Friends on this Server'),
                      ('5','Friends'))

    CONTENT_TYPE_CHOICES = (('text/plain', 'Plain text'),
                            ('text/x-markdown', 'Markdown'),
                            ('text/html', 'HTML'))

    uuid = models.CharField(max_length=36, default = uuid.uuid4)
    title = models.CharField(max_length=128, blank=True)
    description = models.CharField(max_length=512, blank=True)
    content_type = models.CharField(max_length=32, choices=CONTENT_TYPE_CHOICES)
    post_text = models.TextField(max_length=2048)
    image = models.ImageField(upload_to='post_images', blank=True)
    author = models.ForeignKey(Profile)
    date = models.DateTimeField('date posted')
    privacy = models.CharField(max_length=1, choices=PRIVACY_CHOICES)
    allowed=models.ManyToManyField(Profile,null=True,blank=True, related_name="allowed")

    def get_image_path(self):
        return self.image.path
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
