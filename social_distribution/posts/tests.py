from django.test import TestCase, Client
from posts.models import Post
from authors.models import Profile
from django.contrib.auth.models import User
from django.utils import timezone
from posts.forms import PostForm,EditForm
from nodes.models import Host
import base64
import json

# Create your tests here.
class PostTestCase(TestCase):
    def setUp(self):
        date = timezone.now()
        user = User.objects.create(username="test_user1")
        user.set_password("password1")
        user.save()
        user2 = User.objects.create(username="test_user2")
        user2.set_password("password2")
        user2.save()
        user3 = User.objects.create(username="test_user3")
        user3.set_password("password3")
        user3.save()
        profile = Profile.objects.create(user=user, displayname="John")
        profile2 = Profile.objects.create(user=user2, displayname="John2")
        profile3 = Profile.objects.create(user=user3, displayname="John3")
        Post.objects.create(title="test1",description="d1",post_text="p1",author=profile, privacy="1",date=date)
        Post.objects.create(title="test2",description="d2",post_text="p2",author=profile, privacy="2",date=date)
        Post.objects.create(title="test3",description="d3",post_text="p3",author=profile, privacy="3",date=date)
        Post.objects.create(title="test4",description="d4",post_text="p4",author=profile, privacy="4",date=date)
        Post.objects.create(title="test5",description="d5",post_text="p5",author=profile, privacy="1",date=date, image="post_images/image1.png")
        Post.objects.create(title="test6",description="d6",post_text="p6",author=profile, privacy="2",date=date, image="post_images/image2.png")
        Post.objects.create(title="test7",description="d7",post_text="p7",author=profile, privacy="3",date=date, image="post_images/image3.png")
        Post.objects.create(title="test8",description="d8",post_text="p8",author=profile, privacy="4",date=date, image="post_images/image4.png")
        Post.objects.create(title="test9",description="d9",post_text="p9",author=profile, privacy="5",date=date, image="post_images/image5.png")

        Host.objects.create(name="TestHost",share=True,host_url="http://127.0.0.1:8000",username="user",password="pass")

        self.client = Client()

    def test_posts(self):
	
        user1 = User.objects.get(username="test_user1")
        user2 = User.objects.get(username="test_user2")
        user3 = User.objects.get(username="test_user3")

        post1 = Post.objects.get(title="test1")
        post2 = Post.objects.get(title="test2")
        post3 = Post.objects.get(title="test3")
        post4 = Post.objects.get(title="test4")
        post5 = Post.objects.get(title="test5")
        post6 = Post.objects.get(title="test6")
        post7 = Post.objects.get(title="test7")
        post8 = Post.objects.get(title="test8")
        post9 = Post.objects.get(title="test9")
	
        # check that the default number in allowed is 0
        self.assertEqual(post5.allowed.all().count(), 0)
        self.assertEqual(post6.allowed.all().count(), 0)
        self.assertEqual(post7.allowed.all().count(), 0)
        self.assertEqual(post8.allowed.all().count(), 0)
        self.assertEqual(post9.allowed.all().count(), 0)
        
        # set 3 users allowed for post3
        post7.allowed.add(Profile.objects.get(user=user1))
        post7.allowed.add(Profile.objects.get(user=user2))
        post7.allowed.add(Profile.objects.get(user=user3))

        # set 1 user allowed for post7
        post8.allowed.add(Profile.objects.get(user=user1))

        #Privacy tests
        # check that there is a correct number of allowed users
        self.assertEqual(post8.allowed.all().count(), 1)
        self.assertEqual(post7.allowed.all().count(), 3)
        
        # make sure the allowed users are the correct ones
        self.assertTrue(Profile.objects.get(user = user1) in post8.allowed.all())
        self.assertFalse(Profile.objects.get(user = user2) in post8.allowed.all())
        self.assertFalse(Profile.objects.get(user = user3) in post8.allowed.all())
        
        self.assertTrue(Profile.objects.get(user = user1) in post7.allowed.all())
        self.assertTrue(Profile.objects.get(user = user2) in post7.allowed.all())
        self.assertTrue(Profile.objects.get(user = user3) in post7.allowed.all())
	'''
        self.assertEqual(post1.privacy, "1")
        self.assertEqual(post2.privacy, "2")
        self.assertEqual(post3.privacy, "3")
        self.assertEqual(post4.privacy, "4")
        self.assertEqual(post5.privacy, "1")
        self.assertEqual(post6.privacy, "2")
        self.assertEqual(post7.privacy, "3")
        self.assertEqual(post8.privacy, "4")
	'''


        #Editing tests
        #Test edit title
	'''
        self.assertEqual(post1.title, "test1")
        post1.title = "change1"
        self.assertEqual(post1.title, "change1")

        #Test edit body
        self.assertEqual(post1.post_text,"p1")
        post1.post_text = "change2"
        self.assertEqual(post1.post_text,"change2")

        #Test edit description
        self.assertEqual(post2.description,"d2")
        post1.description = "change3"
        self.assertEqual(post1.description,"change3")

        #Test edit privacy
        self.assertEqual(post2.privacy,"2")
        post2.privacy = "1"
        self.assertEqual(post2.privacy,"1")
	'''
        #Test edit image - remove
        self.assertEqual(post5.image,"post_images/image1.png")
        post5.image = ""
        self.assertEqual(post5.image,"")

        #Test edit image - replace
        self.assertEqual(post6.image,"post_images/image2.png")
        post6.image = "new_image.png"
        self.assertEqual(post6.image,"new_image.png")

        #Test edit image - add
        self.assertEqual(post1.image,"")
        post1.image = "post_images/add_image.png"
        self.assertEqual(post1.image,"post_images/add_image.png")

        #Test edit effect on image
        self.assertEqual(post7.title, "test7")
        self.assertEqual(post7.image,"post_images/image3.png")
        post7.title = "change1"
        self.assertEqual(post7.title, "change1")
        self.assertEqual(post7.image,"post_images/image3.png")


    def test_api(self):
        self.client.login(username="test_user1", password="password1")
        user = User.objects.get(username="test_user1")

        #Test authorization
        response = self.client.get('/api/posts/')
        self.assertEqual(response.status_code, 401)

        auth = "Basic " + base64.b64encode("user:pass")
        response = self.client.get('/api/posts/', HTTP_AUTHORIZATION=auth)
        self.assertEqual(response.status_code, 200)

        #Test /api/author/posts/
        response = self.client.get('/api/author/posts/', HTTP_AUTHORIZATION=auth)
        response_json = json.loads(response.content)
        self.assertEqual(response_json['posts'][0]['title'], 'test1')

        #Test /api/posts/
        response = self.client.get('/api/posts/', HTTP_AUTHORIZATION=auth)
        response_json = json.loads(response.content)
        self.assertEqual(response_json['posts'][0]['title'], 'test1')

        #Test /api/author/{AUTHOR ID}/posts
        author_id = Profile.objects.get(displayname="John").uuid
        response = self.client.get('/api/author/'+author_id+'/posts/', HTTP_AUTHORIZATION=auth)
        response_json = json.loads(response.content)
        self.assertEqual(response_json['posts'][0]['title'], 'test1')
        #Test invalid author id
        response = self.client.get('/api/author/SHOULD_NOT_WORK/posts/', HTTP_AUTHORIZATION=auth)
        self.assertEqual(response.status_code, 404)

        #Test /api/posts/{POST_ID}
        post_id = Post.objects.get(title="test1").uuid
        response = self.client.get('/api/posts/'+post_id+'/', HTTP_AUTHORIZATION=auth)
        response_json = json.loads(response.content)
        self.assertEqual(response_json['posts'][0]['title'], 'test1')
        #Test invalid post
        response = self.client.get('/api/posts/NOT_VALID_POST_ID/', HTTP_AUTHORIZATION=auth)
        self.assertEqual(response.status_code, 404)

        #Test /api/post
        profile_id = Profile.objects.get(displayname='John').uuid
        post_data = {'title':'New post', 'description':'Look at this',
        'content':'This is the content', 'content-type':'plaintext'}
        post_string = json.dumps(post_data)
        response = self.client.post('/api/post/', \
        content_type='application/json', data=post_string, HTTP_AUTHORIZATION=auth)
        self.assertEqual(Post.objects.count(), 10)


#Testing EditForm and PostForm
class FormTestCase(TestCase):
    def setUp(self):
        date = timezone.now()
        user = User.objects.create(username="test_user2")
        profile = Profile.objects.create(user=user)
        Post.objects.create(uuid="1",title="test5",description="d1",post_text="p1",author=profile, privacy="1",date=date)
        self.client = Client()

    def test_forms(self):
        user = User.objects.get(username="test_user2")
        post = Post.objects.get(uuid="1")

        #Test minimum form data required
        form_data={"post_text":"body", "privacy":"1","content_type":"text/plain"}
        form = PostForm(user,data=form_data)
        self.assertEqual(form.is_valid(),True)

        #Test missing body
        form_data2={"privacy":"1"}
        form = PostForm(user,data=form_data2)
        self.assertEqual(form.is_valid(),False)

        #Test missing privacy
        form_data3={"post_text":"body"}
        form = PostForm(user,data=form_data3)
        self.assertEqual(form.is_valid(),False)

        #Test all options
        form_data4 = {"title":"t1", "post_text":"p1","description":"d1", "privacy":"1", "image":"post_images/image.png", "content_type":"text/plain","content_type":"text/plain"}
        form = PostForm(user,data=form_data4)
        self.assertEqual(form.is_valid(),True)
	'''
        #Test privacy = 2
        form_data5 = {"title":"t1", "post_text":"p1","description":"d1", "privacy":"2", "image":"post_images/image.png","content_type":"text/plain"}
        form = PostForm(user,data=form_data5)
        self.assertEqual(form.is_valid(),True)

        #Test privacy = 3
        form_data6 = {"title":"t1", "post_text":"p1","description":"d1", "privacy":"3", "image":"post_images/image.png","content_type":"text/plain"}
        form = PostForm(user,data=form_data6)
        self.assertEqual(form.is_valid(),True)

        #Test privacy = 4
        form_data7 = {"title":"t1", "post_text":"p1","description":"d1", "privacy":"4", "image":"post_images/image.png","content_type":"text/plain"}
        form = PostForm(user,data=form_data7)
        self.assertEqual(form.is_valid(),True)
	'''
        #Test non-valid privacy
        form_data8 = {"title":"t1", "post_text":"p1","description":"d1", "privacy":"6", "image":"post_images/image.png"}
        form = PostForm(user,data=form_data8)
        self.assertEqual(form.is_valid(),False)

        #Test assorted combinations
        form_data9 = {"title":"t2", "post_text":"p2","description":"d2", "privacy":"4","content_type":"text/plain"}
        form = EditForm(user,post,data=form_data9)
        self.assertEqual(form.is_valid(),True)

        form_data10={"title":"post with image", "post_text":"d3", "privacy":"1","content_type":"text/plain"}
        form = PostForm(user,data=form_data10)
        self.assertEqual(form.is_valid(),True)

        form_data11={"title":"t1", "description":"d1", "privacy":"1","content_type":"text/plain"}
        form = PostForm(user,data=form_data11)
        self.assertEqual(form.is_valid(),False)

        form_data12={"post_text":"body", "privacy":"1","content_type":"text/plain"}
        form = PostForm(user,data=form_data12)
        self.assertEqual(form.is_valid(),True)

	#No content type
	form_data12={"post_text":"body", "privacy":"1"}
        form = PostForm(user,data=form_data12)
        self.assertEqual(form.is_valid(),False)

        #Test can connect to posts.html
        response = self.client.get('/posts/')
        self.assertTrue(response.status_code==200 or response.status_code==302 or response.status_code==301)

        #Test that I can edit post with id=1
        response = self.client.get('/edit/post/1')
	self.assertTrue(response.status_code==200 or response.status_code==302 or response.status_code==301)

	#Test expand_post.html
	response = self.client.get('/posts/1')
	self.assertTrue(response.status_code==200 or response.status_code==302 or response.status_code==301)

	#Test delete post
	response=self.client.get('/delete/post/1')
	self.assertTrue(response.status_code==200 or response.status_code==302 or response.status_code==301)

	#Test view posts
	response=self.client.get('/posts/all')
	self.assertTrue(response.status_code==200 or response.status_code==302 or response.status_code==301)

	response=self.client.get('/posts/friends')
	self.assertTrue(response.status_code==200 or response.status_code==302 or response.status_code==301)

	response=self.client.get('/author/{{ profile.uuid }}/posts')
	self.assertTrue(response.status_code==200 or response.status_code==302 or response.status_code==301)

