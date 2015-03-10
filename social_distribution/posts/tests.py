from django.test import TestCase, Client
from posts.models import Post
from authors.models import Profile
from django.contrib.auth.models import User
from django.utils import timezone
from posts.forms import PostForm,EditForm

# Create your tests here.
#Gives a warning because Django prefers timezone over datetime but tests
#still run fine
class PostTestCase(TestCase):
    def setUp(self):
        date = timezone.now()
        user = User.objects.create(username="test_user1")
        user.set_password("password1")
        user.save()
        profile = Profile.objects.create(user=user, displayname="John")
        Post.objects.create(title="test1",description="d1",post_text="p1",author=profile, privacy="1",date=date)
        Post.objects.create(title="test2",description="d2",post_text="p2",author=profile, privacy="2",date=date)
        Post.objects.create(title="test3",description="d3",post_text="p3",author=profile, privacy="3",date=date)
        Post.objects.create(title="test4",description="d4",post_text="p4",author=profile, privacy="4",date=date)
        self.client = Client()

    def test_posts(self):
        post1 = Post.objects.get(title="test1")
        post2 = Post.objects.get(title="test2")
        post3 = Post.objects.get(title="test3")
        post4 = Post.objects.get(title="test4")

        #Privacy tests
        self.assertEqual(post1.privacy, "1")
        self.assertEqual(post2.privacy, "2")
        self.assertEqual(post3.privacy, "3")
        self.assertEqual(post4.privacy, "4")

        #Editing tests
        self.assertEqual(post1.title, "test1")
        post1.title = "change1"
        self.assertEqual(post1.title, "change1")
        self.assertEqual(post1.post_text,"p1")
        post1.post_text = "change2"
        self.assertEqual(post1.post_text,"change2")
        self.assertEqual(post2.description,"d2")
        post1.description = "change3"
        self.assertEqual(post1.description,"change3")
        self.assertEqual(post2.privacy,"2")
        post2.privacy = "1"
        self.assertEqual(post2.privacy,"1")

    def test_api(self):
        self.client.login(username="test_user1", password="password1")

        #Test /api/author/posts/
        response = self.client.get('/api/author/posts/')
        self.assertEqual(response['Content-Type'], 'application/json')

        #Test /api/posts/
        response = self.client.get('/api/posts/')
        self.assertEqual(response['Content-Type'], 'application/json')

        #Test /api/author/{AUTHOR ID}/posts
        author_id = Profile.objects.get(displayname="John").uuid
        response = self.client.get('/api/author/'+author_id+'/posts/')
        self.assertEqual(response['Content-Type'], 'application/json')
        #Test invalid author id
        response = self.client.get('/api/author/SHOULD_NOT_WORK/posts/')
        self.assertEqual(response.status_code, 404)

        #Test /api/posts/{POST_ID}
        post_id = Post.objects.get(title="test1").uuid
        response = self.client.get('/api/posts/'+post_id+'/')
        self.assertEqual(response['Content-Type'], 'application/json')
        #Test invalid post
        response = self.client.get('/api/posts/NOT_VALID_POST_ID/')
        self.assertEqual(response.status_code, 404)


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

        form_data = {"title":"t1", "post_text":"p1","description":"d1", "privacy":"1"}
        form = PostForm(user,data=form_data)
        self.assertEqual(form.is_valid(),True)

        form_data1 = {"title":"t2", "post_text":"p2","description":"d2", "privacy":"4"}
        form = EditForm(user,post,data=form_data1)
        self.assertEqual(form.is_valid(),True)

        form_data2={"title":"t1", "description":"d1", "privacy":"1"}
        form = PostForm(user,data=form_data2)
        self.assertEqual(form.is_valid(),False)

        #Test can connect to posts.html
        response = self.client.get('/posts/')
        self.assertEqual(response.status_code,200)
        #Test that i can edit post with id=1
        response = self.client.get('/edit/post/1')
        self.assertEqual(response.status_code,200)
