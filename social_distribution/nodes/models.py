from django.db import models
import urllib, urllib2
import json

# Create your models here.

class Host(models.Model):
    name = models.CharField(max_length=128)
    host_url = models.CharField(max_length=128)
    # url extensions for accessing API functions
    posts_visible_to_current_user = models.CharField(max_length=64, default='/author/posts/')
    public_posts = models.CharField(max_length=64, default='/posts/')
    all_posts_by_author_visible = models.CharField(max_length=64, default='/author/{AUTH_ID}/posts/')
    get_put_post_postid = models.CharField(max_length=64, default='/posts/{POST_ID}/')
    friend_response = models.CharField(max_length=64, default='/friends/{AUTH1_ID}/{AUTH2_ID}/')
    friend_auth_response = models.CharField(max_length=64, default='/friends/{AUTH_ID}/')
    friend_request = models.CharField(max_length=64, default='/friendrequest/')
    all_authors = models.CharField(max_length=64, default='/authors/')

    def get_posts_visible_to_current_user(self):
        # INCOMPLETE: DOES NOT GET CURRENT USER
        url = self.host_url + self.posts_visible_to_current_user
        json_string = urllib2.urlopen(url).read()
        data = json.loads(json_string)
        return data

    def get_public_posts(self):
        url = self.host_url + self.public_posts
        json_string = urllib2.urlopen(url).read()
        data = json.loads(json_string)
        return data

    def get_all_posts_by_author(self):
        # INCOMPLETE: DOES NOT GET CURRENT USER
        url = self.host_url + self.all_posts_by_author_visible
        json_string = urllib2.urlopen(url).read()
        data = json.loads(json_string)
        return data

    def get_postid(self, postid):
        url = self.host_url + self.get_put_post_postid
        url = url.replace("{POST_ID}", postid)
        json_string = urllib2.urlopen(url).read()
        data = json.loads(json_string)
        return data

    def get_friend_response(self, auth1, auth2):
        url = self.host_url + self.friend_response
        url = url.replace("{AUTH1_ID}", auth1)
        url = url.replace("{AUTH2_ID}", auth2)
        json_string = urllib2.urlopen(url).read()
        data = json.loads(json_string)
        return data

    def post_friend_auth_response(self, author, friends_list):
        url = self.host_url + self.friend_auth_response
        url = url.replace("{AUTH_ID}", author)
        encoded_json = json.dumps(
        {'query':'friends',
        'author': author,
        'authors': friends_list}
        )
        json_string = urllib2.urlopen(url=url, data=encoded_json).read()
        data = json.loads(json_string)
        return data

    def post_friend_request(self, authors_list):
        url = self.host_url + self.friend_request
        encoded_json = json.dumps(
        {'query':'friendrequest',
        'author': {
            'id':authors_list[0],
            'host':"",
            'displayname':""
            },
        'friend': {
            'id':authors_list[1],
            'host':"",
            'displayname':"",
            'url':""
            }
        }
        )
        json_string = urllib2.urlopen(url=url, data=encoded_json).read()
        data = json.loads(json_string)
        return data

    def get_all_authors(self):
        url = self.host_url + self.all_authors
        json_string = urllib2.urlopen(url).read()
        data = json.loads(json_string)
        return data

    def __unicode__(self):
        return str(self.name)
