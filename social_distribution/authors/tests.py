from django.test import TestCase, Client
from django.contrib.auth.models import User
from authors.models import Profile, Follow
from nodes.models import Host
import json
import base64

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

        Host.objects.create(name="TestHost",share=True,host_url="http://127.0.0.1:8000",username="user",password="pass")

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
        auth = "Basic " + base64.b64encode("user:pass")

        #Test /api/authors
        response = self.client.get('/api/authors/',
        HTTP_AUTHORIZATION=auth)
        response_json = json.loads(response.content)
        self.assertEqual(response_json[0]['username'], 'johnsmith')

        #Test /api/friends/{FRIEND1_ID}/{FRIEND2_ID}
        response = self.client.get('/api/friends/'+uuid1+'/'+uuid2+'/',
        HTTP_AUTHORIZATION=auth)
        response_json = json.loads(response.content)
        self.assertEqual(response_json['friends'], 'NO')

        #Test /api/friends/{AUTHOR_ID}
        post_data = {'query':'friends', 'author':uuid1, 'authors': [uuid2, uuid3]}
        post_string = json.dumps(post_data)
        response = self.client.post('/api/friends/'+uuid1+'/',
        content_type='application/json', data=post_string,
        HTTP_AUTHORIZATION=auth)
        response_json = json.loads(response.content)
        self.assertEqual(response_json['friends'], [])
        #Test invalid author
        response = self.client.post('/api/friends/INVALID_ID/',
        content_type='application/json', data=post_string,
        HTTP_AUTHORIZATION=auth)
        self.assertEqual(response.status_code, 404)

        #Test /api/friendrequest
        post_data = {'query':'friendrequest', 'author':{
        'id': uuid1, 'host':'', 'displayname': 'xxxbadb0y23xxx'},
        'friend':{'id':uuid2, 'host':'', 'displayname': 'need_help'}}
        post_string = json.dumps(post_data)
        response = self.client.post('/api/friendrequest/',
        content_type='application/json', data=post_string,
        HTTP_AUTHORIZATION=auth)
        self.assertEqual(Follow.objects.all().count(), 1)
        #Test invalid id
        post_data['author']['id'] = 'INVALID'
        post_string = json.dumps(post_data)
        response = self.client.post('/api/friendrequest/',
        content_type='application/json', data=post_string,
        HTTP_AUTHORIZATION=auth)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(Profile.objects.all().count(), 5)


	#Test HTML responses
	#Test index
	response=self.client.get('/')
	self.assertTrue(response.status_code==200 or response.status_code==302 or response.status_code==301)

	#Test login
	response=self.client.get('/login')
	self.assertTrue(response.status_code==200 or response.status_code==302 or response.status_code==301)
	
	#Test register
	response=self.client.get('/register')
	self.assertTrue(response.status_code==200 or response.status_code==302 or response.status_code==301)

	#Test manage profile page
	response=self.client.get('/manage')
	self.assertTrue(response.status_code==200 or response.status_code==302 or response.status_code==301)

	#Test view profile page
	response=self.client.get('/author/{{ uuid1.uuid }}')
	self.assertTrue(response.status_code==200 or response.status_code==302 or response.status_code==301)

	#Test add friend page
	response=self.client.get('/add_friend')
	self.assertTrue(response.status_code==200 or response.status_code==302 or response.status_code==301)

	#Test my friends page
	response=self.client.get('/my_friends')
	self.assertTrue(response.status_code==200 or response.status_code==302 or response.status_code==301)

	#Test something that doesn't exist
	response=self.client.get('/does_not_exist')
	self.assertTrue(response.status_code==404)

class FriendsTestCase(TestCase):
    def setUp(self):
        user1 = User.objects.create(username="user1")
        user2 = User.objects.create(username="user2")
        user3 = User.objects.create(username="user3")
        user4 = User.objects.create(username="user4")

        profile1 = Profile.objects.create(user=user1, displayname="user1")
        profile2 = Profile.objects.create(user=user2, displayname="user2")
        profile3 = Profile.objects.create(user=user3, displayname="user3")
        profile4 = Profile.objects.create(user=user4, displayname="user4")

    def test_follow(self):
        profile1 = Profile.objects.get(displayname="user1")
        profile2 = Profile.objects.get(displayname="user2")
        profile3 = Profile.objects.get(displayname="user3")

        testFollow1 = Follow(from_profile_id=profile1, to_profile_id=profile2, status='PENDING')
        testFollow1.save()
        testFollow2 = Follow(from_profile_id=profile2, to_profile_id=profile3, status='FOLLOWING')
        testFollow2.save()

        #See if the two Follow objects are created
        self.assertTrue(Follow.objects.all(),2)

        #A follows B but does not mean B follows A
        self.assertTrue(Follow.objects.get(from_profile_id=profile1, to_profile_id=profile2))

        self.assertFalse(Follow.objects.filter(from_profile_id=profile2, to_profile_id=profile1))

    def test_friendship(self):
        profile1 = Profile.objects.get(displayname="user1")
        profile2 = Profile.objects.get(displayname="user2")
        profile3 = Profile.objects.get(displayname="user3")

        profile1.friends.add(profile2)
        profile1.save()

        #If A and B are friends, then B and A are friends as well.
        self.assertIn(profile2, profile1.friends.all())
        self.assertIn(profile1, profile2.friends.all())

        #C should not be friends with A or B
        self.assertNotIn(profile3, profile1.friends.all())
        self.assertNotIn(profile3, profile2.friends.all())
