from django.db import models

# Create your models here.

class Author(models.Model):
    username = models.CharField(max_length=128)
    password = models.CharField(max_length=128)
    follows = models.ManyToManyField('self', blank=True, symmetrical=False)
    friends = models.ManyToManyField('self', blank=True)

    def __unicode__(self):
        return self.username

class Profile(models.Model):
    GENDER_CHOICES = (('M', 'Male'),
                      ('F', 'Female'))

    author_id = models.OneToOneField(Author)
    name = models.CharField(max_length=128, default='N/A')
    body = models.Field(max_length=2048, blank=True)
    birthdate = models.DateField('birthdate',null=True, blank=True)
    gender = models.CharField(max_length=1, blank=True, choices=GENDER_CHOICES)
    image = models.ImageField(blank=True)
    workspace = models.CharField(max_length=128, blank=True)
    school = models.CharField(max_length=128, blank=True)

    def __unicode__(self):
        return str(self.author_id)
