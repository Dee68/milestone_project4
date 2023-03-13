from django.test import TestCase
from django.urls import reverse
from django.contrib.auth.models import User


class TestRegister(TestCase):
    # @classmethod
    # def setUp(self):
    #     cls.user = get_user_model().objects.create_user(username='username', email='noreply@gmail.com', password='password')

    def test_should_show_register_page(self):
        self.register_url = reverse('account:register')
        self.user = { 
            'username': 'username',
            'email': 'noreply@gmail.com',
            'password1': 'password',
            'password2': 'password'
        }
        response = self.client.get(self.register_url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'account/register.html')

    def test_can_not_register_with_long_username(self):
        self.register_url = reverse('account:register')
        self.user_with_long = { 
            'username': 'username12',
            'email': 'noreply@gmail.com',
            'password1': 'password',
            'password2': 'password'
        }
        response = self.client.post(self.register_url, self.user_with_long, format='text/html')
        self.assertEqual(response.status_code, 406)

    def test_can_not_register_with_invalid_email(self):
        self.register_url = reverse('account:register')
        self.user_with_invalid_email = { 
            'username': 'johnny',
            'email': 'noreply.com',
            'password1': 'password',
            'password2': 'password'
        }
        response = self.client.post(self.register_url, self.user_with_invalid_email, format='text/html')
        self.assertEqual(response.status_code, 400)

    # def test_can_register_user(self):
    #     self.register_url = reverse('account:register')
    #     User = get_user_model()
    #     self.user = {
    #         'username': 'username',
    #         'email': 'noreply@gmail.com',
    #         'password1': 'password',
    #         'password2': 'password' 
    #     }
    #     self.user1 = User.objects.create_user(username=self.user['username'], email=self.user['email'], password=self.user['password1'])   
    #     response = self.client.get(self.register_url)
    #     self.assertEqual(response.status_code, 200)
    #     response = self.client.post(self.register_url, self.user)
    #     # self.assertIsNot(self.user.id, None)
    #     self.assertEqual(response.status_code, 200)

    def test_can_not_register_with_empty_name_and_password(self):
        self.register_url = reverse('account:register')
        self.user = {
            'username': '',
            'email': 'noreply1@gmail.com',
            'password1': '',
            'password2': 'password' 
        }
        response = self.client.post(self.register_url, self.user)
        self.assertEquals(response.status_code, 400)

    def test_can_not_register_user_not_matching_passwords(self):
        self.register_url = reverse('account:register')
        self.user = {
            'username': 'user1',
            'email': 'noreply1@gmail.com',
            'password1': 'password1',
            'password2': 'password2' 
        }
        response = self.client.post(self.register_url, self.user)
        self.assertEquals(response.status_code, 404)

    def test_can_not_register_user_not_missing_passwords(self):
        self.register_url = reverse('account:register')
        self.user = {
            'username': 'user1',
            'email': 'noreply1@gmail.com',
            'password1': '',
            'password2': '' 
        }
        response = self.client.post(self.register_url, self.user)
        self.assertEquals(response.status_code, 400)

    def test_can_not_register_user_with_non_alhanumeric(self):
        self.register_url = reverse('account:register')
        self.user = {
            'username': 'user#',
            'email': 'noreply1@gmail.com',
            'password1': 'password',
            'password2': 'password' 
        }
        response = self.client.post(self.register_url, self.user)
        self.assertEquals(response.status_code, 400)

    # def test_can_not_register_user_with_taken_email(self):
    #     self.register_url = reverse('account:register')
    #     self.user = {
    #         'username': 'user',
    #         'email': 'noreply@gmail.com',
    #         'password1': 'password',
    #         'password2': 'password' 
    #     }
    #     self.user1 = {
    #         'username': 'user1',
    #         'email': 'noreply@gmail.com',
    #         'password1': 'password',
    #         'password2': 'password' 
    #     }
    #     self.client.post(self.register_url, self.user)
    #     response = self.client.post(self.register_url, self.user1)
    #     self.assertEquals(response.status_code, 409)

    def test_should_show_login_page(self):
        response = self.client.get(reverse('account:signin'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'account/signin.html')

    def test_should_login_user_with_correct_credentials(self):
        self.user = {
            'username': 'username',
            'email': 'noreply@gmail.com',
            'password1': 'password',
            'password2': 'password'
        }
        self.register_url = reverse('account:register')
        self.login_url = reverse('account:signin')
        self.client.post(self.register_url, self.user)
        user = User.objects.filter(email=self.user['email'])
        user.save()
        response = self.client.post(self.login_url, self.user)
        self.assertEquals(response.status_code, 200)


    def test_should_not_login_user_with_empty_credentials(self):
        self.user = {
            'username': '',
            'password': ''
        }
        response = self.client.post(reverse('account:signin'), self.user)
        self.assertEqual(response.status_code, 401)
