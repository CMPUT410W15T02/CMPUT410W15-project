from django.test import TestCase
from django.contrib.auth.models import User
from authors.models import Profile

# Create your tests here.

class AuthorTestCase(TestCase):
    def setUp(self):
        user1 = User.objects.create(username="johnsmith", password="abc", is_active=False)
        Profile.objects.create(user=user1, displayname="xxxbadb0y23xxx")

        user2 = User.objects.create(username="aTest", password="12345", is_active=False)
        Profile.objects.create(user=user2, displayname="need_help")

        user3 = User.objects.create(username="oneMore", password="zzzz", is_active=False)
        Profile.objects.create(user=user3, displayname="good name")

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
