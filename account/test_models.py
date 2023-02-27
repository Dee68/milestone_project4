from django.test import TestCase
from .models import Profile
from django.contrib.auth import get_user_model


class TestModels(TestCase):
    def test_should_create_user_profile(self):
        User = get_user_model()
        user = User.objects.create_user(username='username', first_name='fname', last_name='lname', email='email@gmail.com', password='password')
        user.set_password('password')
        user.save()
        pr = Profile.objects.get(user=user)
        self.assertEqual(str(pr), f"{user.username}'s profile")
