from django.test import TestCase
from posts.models import Post
from authors.models import Profile
from django.contrib.auth.models import User
from django.utils import unittest
from datetime import datetime
from posts.forms import PostForm,EditForm
from django.test import Client
# Create your tests here.
#Gives a warning because Django prefers timezone over datetime but tests
#still run fine
class PostTestCase(unittest.TestCase):
    def setUp(self):
        self.date=datetime.now()
        self.user=User.objects.create(username="test_user",password="whyisthisnecessary?")
        self.profile=Profile.objects.create(user=self.user)
        
        self.post1=Post.objects.create(title="test1",description="d1",post_text="p1",author=self.profile, privacy="1",date=self.date)
        
        self.post2=Post.objects.create(title="test2",description="d2",post_text="p2",author=self.profile, privacy="2",date=self.date)
        
        self.post3=Post.objects.create(title="test3",description="d3",post_text="p3",author=self.profile, privacy="3",date=self.date)
        
        self.post4=Post.objects.create(title="test4",description="d4",post_text="p4",author=self.profile, privacy="4",date=self.date)
    def testPosts(self):
        #Privacy tests
        self.assertEqual(self.post1.privacy, "1")
        self.assertEqual(self.post2.privacy, "2")
        self.assertEqual(self.post3.privacy, "3")
        self.assertEqual(self.post4.privacy, "4")
        
        #Editing tests
        self.assertEqual(self.post1.title, "test1")
        self.post1.title="change1"
        self.assertEqual(self.post1.title, "change1")
        self.assertEqual(self.post1.post_text,"p1")
        self.post1.post_text="change2"
        self.assertEqual(self.post1.post_text,"change2")
        self.assertEqual(self.post2.description,"d2")
        self.post1.description="change3"
        self.assertEqual(self.post1.description,"change3")        
        self.assertEqual(self.post2.privacy,"2")
        self.post2.privacy="1"
        self.assertEqual(self.post2.privacy,"1")

#Testing EditForm and PostForm
class FormTestCase(unittest.TestCase):
    def setUp(self):
        self.date=datetime.now()
        self.user=User.objects.create(username="test_user1",password="whyisthisnecessary?")    
        self.profile=Profile.objects.create(user=self.user)
        self.post=Post.objects.create(uuid="1",title="test1",description="d1",post_text="p1",author=self.profile, privacy="1",date=self.date)
        self.client=Client()
    def test_forms(self):
        form_data={"title":"t1", "post_text":"p1","description":"d1", "privacy":"1"}
        form=PostForm(self.user,data=form_data)
        self.assertEqual(form.is_valid(),True)
        
        form_data1={"title":"t2", "post_text":"p2","description":"d2", "privacy":"4"}
        form=EditForm(self.user,self.post,data=form_data1)
        self.assertEqual(form.is_valid(),True)        
        
        form_data2={"title":"t1", "description":"d1", "privacy":"1"}
        form=PostForm(self.user,data=form_data2)
        self.assertEqual(form.is_valid(),False)      
        
        #Test can connect to posts.html
        response=self.client.get('/posts/')
        self.assertEqual(response.status_code,200)
        #Test that i can edit post with id=1 
        response=self.client.get('/edit/post/1')
        self.assertEqual(response.status_code,200)        