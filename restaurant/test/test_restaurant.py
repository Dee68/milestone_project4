from django.test import TestCase
from django.urls import reverse
from django.core.files.uploadedfile import SimpleUploadedFile
from django.contrib.messages import get_messages
from django.contrib.auth.models import User
from restaurant.models import Table, Reservation, TableImage


class BaseTest(TestCase):
    def setUp(self):
        # self.newPhoto.image = SimpleUploadedFile(name='test_image.jpg', content=open(image_path, 'rb').read(), content_type='image/jpeg')
        self.home_url = reverse('restaurant:home')
        self.reservation_url = reverse('restaurant:reservations')
        # self.table_detail_url = reverse('restaurant:table-detail', kwargs={'id':id, 'slug':slug})
        self.table = {
            'id': 1,
            'title': 'table',
            'table_type': 'basic',
            'number': 101,
            'capacity': 4,
            'cost': 100.00,
            'slug': 'title',
            'image':'image',
            'is_available': True,
            'description': 'Some text goes here ...'
        }
        # self.table_image = {
        #     'table': self.table,
        #     'images':'image'
        # }
        return super().setUp()
        

class TableTest(BaseTest):
    def test_show_home_page(self):
        response = self.client.get(self.home_url)
        self.assertTemplateUsed(response, 'restaurant/index.html')
        self.assertEqual(response.status_code, 200)

    def test_should_create_table(self):
        user_table = Table.objects.create(**self.table)
        user_table.save()
        self.assertEqual(str(user_table), f"Table number {self.table['number']} with a capacity of {self.table['capacity']}")

    def test_should_create_table_image(self):
        user_table = Table.objects.create(**self.table)
        table_image = TableImage.objects.create(table=user_table, images='images')
        table_image.save()
        self.assertEqual(str(table_image), user_table.title)

    def test_should_go_to_detail_page(self):
        user_table = Table.objects.create(**self.table)
        user_table.save()
        response = self.client.get(user_table.get_absolute_url())
        self.assertEqual(response.status_code, 200)


class ReservationTest(BaseTest):
    pass