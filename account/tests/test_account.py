from django.test import TestCase
from django.urls import reverse
# from django.contrib.auth import get_user_model
# from account.models import Profile


class BaseTest(TestCase):
    def setUp(self):
        self.register_url = reverse('account:register')
        self.user = { 
            'username': 'username',
            'firstname': 'firstname',
            'lastname': 'lastname',
            'email': 'noreply@gmail.com',
            'password1': 'password',
            'password2': 'password'
        }
        self.user_with_long = {
            'username': 'username12',
            'firstname': 'firstname',
            'lastname': 'lastname',
            'email': 'noreply@gmail.com',
            'password1': 'password',
            'password2': 'password'
        }
        self.user_with_invalid_email = {
            'username': 'username',
            'firstname': 'firstname',
            'lastname': 'lastname',
            'email': 'noreply.com',
            'password1': 'password',
            'password2': 'password'
        }
        return super().setUp()


class RegisterTest(BaseTest):
    def test_should_show_register_page(self):
        response = self.client.get(self.register_url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'account/register.html')

    def test_can_register_user(self):
        response = self.client.post(self.register_url, self.user, format='text/html', follow=True)
        self.assertEqual(response.status_code, 302)

    def test_can_not_register_with_long_username(self):
        response = self.client.post(self.register_url, self.user_with_long, format='text/html')
        self.assertEqual(response.status_code, 400)

    def test_can_not_register_with_invalid_email(self):
        response = self.client.post(self.register_url, self.user_with_invalid_email, format='text/html')
        self.assertEqual(response.status_code, 400)

    def test_can_not_register_user_taken_email_or_username(self):
        self.client.post(self.register_url, self.user, format='text/html', follow=True)
        response = self.client.post(self.register_url, self.user, format='text/html', follow=True)
        self.assertEqual(response.status_code, 409)

    # def test_should_show_login_page(self):
    #     response = self.client.get(reverse('account:signin'))
    #     self.assertEqual(response.status_code, 200)
    #     self.assertTemplateUsed(response, 'account/signin.html')

    # def test_should_not_register_user(self):
    #     self.user = {
        #     'username': '',
        #     'firstname': 'firstname',
        #     'lastname': 'lastname',
        #     'email': 'noreply@gmail.com',
        #     'password1': 'password',
        #     'password2': 'password'
        # }
    #     response = self.client.post(reverse('account:register'), self.user)
    #     self.assertEquals(response.status_code, 400)
    # class TestModels(TestCase):
    # def test_should_create_user_profile(self):
    #     User = get_user_model()
    #     user = User.objects.create_user(username='username', first_name='fname', last_name='lname', email='email@gmail.com', password='password')
    #     user.set_password('password')
    #     user.save()
    #     pr = Profile.objects.get(user=user)
    #     self.assertEqual(str(pr), f"{user.username}'s profile")
