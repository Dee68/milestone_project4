from django.test import TestCase
from django.urls import reverse


class TestViews(TestCase):
    def test_should_show_register_page(self):
        response = self.client.get(reverse('account:register'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'account/register.html')

    def test_should_show_login_page(self):
        response = self.client.get(reverse('account:signin'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'account/signin.html')
