from django.test import TestCase
from django.urls import reverse

class TestRegister(TestCase):
    def test_should_show_register_page(self):
        self.register_url = reverse('account:register')
        self.user = { 
            'username': 'username',
            'firstname': 'firstname',
            'lastname': 'lastname',
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
            'firstname': 'firstname',
            'lastname': 'lastname',
            'email': 'noreply@gmail.com',
            'password1': 'password',
            'password2': 'password'
        }
        response = self.client.post(self.register_url, self.user_with_long, format='text/html')
        self.assertEqual(response.status_code, 400)

    def test_can_not_register_with_invalid_email(self):
        self.register_url = reverse('account:register')
        self.user_with_invalid_email = { 
            'username': 'johnny',
            'firstname': 'firstname',
            'lastname': 'lastname',
            'email': 'noreply.com',
            'password1': 'password',
            'password2': 'password'
        }
        response = self.client.post(self.register_url, self.user_with_invalid_email, format='text/html')
        self.assertEqual(response.status_code, 400)

    def test_should_show_login_page(self):
        response = self.client.get(reverse('account:signin'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'account/signin.html')

    def test_can_register_user(self):
        self.register_url = reverse('account:register')
        self.user = { 
            'username': 'user12',
            'firstname': 'firstname',
            'lastname': 'lastname',
            'email': 'noreply@gmail.com',
            'password1': 'password',
            'password2': 'password'
        }
        response = self.client.post(self.register_url, self.user, format='text/html', follow=True)
        print(response.status_code)
        # self.assertRedirects(response, reverse('account:signin'), status_code=302, target_status_code=200,fetch_redirect_response=True)
        # # self.assertEqual(response.status_code, 302)
        # self.assertContains(response, 'Account successfully created, you can now log in.')
