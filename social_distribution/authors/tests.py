from django.test import TestCase, Client
from django.contrib.auth.models import User
from authors.models import Profile, Follow
import json

# Create your tests here.

class AuthorTestCase(TestCase):
    def setUp(self):
        user1 = User.objects.create(username="johnsmith", is_active=False)
        user1.set_password("abc")
        user1.save()
        Profile.objects.create(user=user1, displayname="xxxbadb0y23xxx")

        user2 = User.objects.create(username="aTest", is_active=False)
        user2.set_password("12345")
        user2.save()
        Profile.objects.create(user=user2, displayname="need_help")

        user3 = User.objects.create(username="oneMore", is_active=False)
        user3.set_password("zzzz")
        user3.save()
        Profile.objects.create(user=user3, displayname="good name")

        self.client = Client()

    def test_multi_users(self):
        user_count = User.objects.all().count()
        self.assertEqual(user_count, 3)

    def test_add_users(self):
        user4 = User.objects.create(username="The4th", password="nice")
        Profile.objects.create(user=user4, displayname="the coolest")

        user_count = User.objects.all().count()
        self.assertEqual(user_count, 4)

    def test_modify_users(self):
        modify_user = User.objects.get(username="oneMore")
        modify_profile = Profile.objects.get(user=modify_user)
        modify_profile.displayname = "changed name!"

        self.assertEqual(modify_profile.displayname, "changed name!")

    def test_delete_users(self):
        delete_user = User.objects.get(username="aTest")
        delete_user.delete()

        user_count = User.objects.all().count()
        self.assertEqual(user_count, 2)

    def test_active_user(self):
        user = User.objects.get(username="johnsmith")
        self.assertEqual(user.is_active, False)
        user.is_active = True
        self.assertEqual(user.is_active, True)

    def test_api(self):
        uuid1 = Profile.objects.get(displayname="xxxbadb0y23xxx").uuid
        uuid2 = Profile.objects.get(displayname="need_help").uuid
        uuid3 = Profile.objects.get(displayname="good name").uuid

        #Test /api/authors
        response = self.client.get('/api/authors/')
        self.assertEqual(response['Content-Type'], 'application/json')

        #Test /api/friends/{FRIEND1_ID}/{FRIEND2_ID}
        response = self.client.post('/api/friends/'+uuid1+'/'+uuid2+'/')
        self.assertEqual(response['Content-Type'], 'application/json')

        #Test /api/friends/{AUTHOR_ID}
        post_data = {'query':'friends', 'author':uuid1, 'authors': [uuid2, uuid3]}
        post_string = json.dumps(post_data)
        response = self.client.post('/api/friends/'+uuid1+'/',
        content_type='application/json', data=post_string)
        self.assertEqual(response['Content-Type'], 'application/json')
        #Test invalid author
        response = self.client.post('/api/friends/INVALID_ID/',
        content_type='application/json', data=post_string)
        self.assertEqual(response.status_code, 404)

        #Test /api/friendrequest
        post_data = {'query':'friendrequest', 'author':{
        'id': uuid1, 'host':'', 'displayname': 'xxxbadb0y23xxx'},
        'friend':{'id':uuid2, 'host':'', 'displayname': 'need_help'}}
        post_string = json.dumps(post_data)
        response = self.client.post('/api/friendrequest/',
        content_type='application/json', data=post_string)
        self.assertEqual(Follow.objects.all().count(), 1)
        #Test invalid id
        post_data['author']['id'] = 'INVALID'
        post_string = json.dumps(post_data)
        response = self.client.post('/api/friendrequest/',
        content_type='application/json', data=post_string)
        self.assertEqual(response.status_code, 404)
