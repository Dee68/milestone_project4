from django.test import TestCase
from django.urls import reverse
from django.contrib.auth.models import User
from django.core.files.uploadedfile import SimpleUploadedFile
from django.contrib.messages import get_messages
from django.contrib.auth.models import User
from django.utils.timezone import now
from django.utils.safestring import mark_safe 
from restaurant.models import Table, Reservation, TableImage, Food, Drink, Review
from datetime import datetime
import pytz


class BaseTest(TestCase):
    def setUp(self):
        self.home_url = reverse('restaurant:home')
        self.reservation_url = reverse('restaurant:reservations')
        self.table_to_reserve_url = reverse('restaurant:table-detail', args=[1,'title'])
        self.table_to_review_url = reverse('restaurant:table-review', args=[1,'title'])
        self.reservation_to_edit = reverse('restaurant:reservation-edit', args=[1])
        self.reservation_delete = reverse('restaurant:reservation-delete', args=[1])
        self.register_url = reverse('account:register')
        self.login_url = reverse('account:signin')
        self.logout_url = reverse('account:logout')
        self.confirm_url = reverse('account:confirmation')
        self.profile_url = reverse('account:profile')
        self.update_profile_url = reverse('account:update-profile')
        self.food_list_url = reverse('restaurant:foods')
        self.drink_list_url = reverse('restaurant:drinks')
        self.review_list_url = reverse('restaurant:reviews')
        self.login_user_url = reverse('restaurant:login-user')
        self.empty_reservation_input = {
            'reserve_start': '',
            'reserve_end': ''
        }
        r_start = '09/18/2020 04:30 PM'
        r_end = '09/18/2020 10:30 PM'
        rr_s = datetime.strptime(r_start, '%m/%d/%Y %I:%M %p').replace(tzinfo=pytz.utc)
        rr_end = datetime.strptime(r_end, '%m/%d/%Y %I:%M %p').replace(tzinfo=pytz.utc)
        self.past_reservation_input = {
            'reserve_start': rr_s.strftime('%m/%d/%Y %I:%M %p') ,
            'reserve_end': rr_end.strftime('%m/%d/%Y %I:%M %p')
        }
        rc_s = '07/10/2023 05:00 PM'
        rc_end = '07/10/2023 11:00 PM'
        rcc_s = datetime.strptime(rc_s, '%m/%d/%Y %I:%M %p').replace(tzinfo=pytz.utc)
        rcc_end = datetime.strptime(rc_end, '%m/%d/%Y %I:%M %p').replace(tzinfo=pytz.utc)
        self.correct_reservation_input = {
            'reserve_start': rcc_s.strftime('%m/%d/%Y %I:%M %p'),
            'reserve_end': rcc_end.strftime('%m/%d/%Y %I:%M %p')
        }
        re_s = '08/10/2023 05:00 PM'
        re_end = '08/10/2023 11:00 PM'
        ree_s = datetime.strptime(re_s, '%m/%d/%Y %I:%M %p').replace(tzinfo=pytz.utc)
        ree_end = datetime.strptime(re_end, '%m/%d/%Y %I:%M %p').replace(tzinfo=pytz.utc)
        self.edit_correct_reservation = {
            'reserve_start': ree_s.strftime('%m/%d/%Y %I:%M %p'),
            'reserve_end': ree_end.strftime('%m/%d/%Y %I:%M %p')
        }
        rt_s = '07/10/2023 06:00 PM'
        rt_end = '07/10/2023 09:30 PM'
        rtt_s = datetime.strptime(rt_s, '%m/%d/%Y %I:%M %p').replace(tzinfo=pytz.utc)
        rtt_end = datetime.strptime(rt_s, '%m/%d/%Y %I:%M %p').replace(tzinfo=pytz.utc)
        self.not_available_reservation = {
            'reserve_start': rtt_s.strftime('%m/%d/%Y %I:%M %p'),
            'reserve_end': rtt_end.strftime('%m/%d/%Y %I:%M %p')
        }
        self.user = {
            'username':'username',
            'email':'noreply@gmail.com',
            'password1':'password',
            'password2':'password'
        }
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
        self.table_without_image = {
           'id': 2,
            'title': 'table',
            'table_type': 'basic',
            'number': 101,
            'capacity': 4,
            'cost': 100.00,
            'slug': 'title',
            'image':'',
            'is_available': True,
            'description': 'Some text goes here ...' 
        }
        self.food = {
            'name':'name',
            'description':'description',
            'food_type':'dessert',
            'price':12.00,
            'image':'image'
        }
        self.food_without_image = {
            'name':'name',
            'description':'description',
            'food_type':'dessert',
            'price':12.00,
            'image':''
        }
        self.drink = {
            'name':'name',
            'description':'description',
            'drink_type':'wine',
            'price':12.00,
            'image':'image'
        }

        self.drink_without_image = {
            'name':'name',
            'description':'description',
            'drink_type':'wine',
            'price':12.00,
            'image':''
        }
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

    def test_should_show_image(self):
        user_table = Table.objects.create(**self.table)
        user_table.save()
        self.assertEqual(user_table.image_tag(),  mark_safe('<img src="%s" height="50" width="50">' %user_table.image.url))

    def test_should_show_no_image(self):
        table = Table.objects.create(**self.table_without_image)
        table.save()
        self.assertEqual(table.image_tag(), 'No image found')

    def test_should_go_to_detail_page(self):
        user_table = Table.objects.create(**self.table)
        user_table.save()
        response = self.client.get(user_table.get_absolute_url())
        self.assertEqual(response.status_code, 200)

    def test_show_login_user_page(self):
        response = self.client.get(self.login_user_url)
        self.assertTemplateUsed(response, 'restaurant/login_user.html')
        self.assertEqual(response.status_code, 200)


class ReservationTest(BaseTest):
    def test_show_reservation_page(self):
        self.client.post(self.register_url, self.user, format='text/html')
        username = self.user['username']
        password = self.user['password1']
        self.user_login = {'username': username, 'password': password}
        self.client.post(self.login_url, self.user_login)
        user_table = Table.objects.create(**self.table)
        user_table.save()
        response = self.client.get(self.reservation_url)
        self.assertTemplateUsed(response, 'restaurant/reservation_list.html')
        self.assertEqual(response.status_code, 200)

    def test_should_create_reservation(self):
        user_table = Table.objects.create(**self.table)
        customer = User.objects.create_user(username='testme', email='noreply@gmail.com', password='password')
        r_start = '2023-09-10 04:30'
        r_end = '2023-09-10 10:00'
        r_s = datetime.strptime(r_start, '%Y-%m-%d %I:%M').replace(tzinfo=pytz.utc)
        r_s = r_s.strftime('%Y-%m-%d %I:%M')
        r_end = datetime.strptime(r_end, '%Y-%m-%d %I:%M').replace(tzinfo=pytz.utc)
        r_end = r_end.strftime('%Y-%m-%d %I:%M')
        reservation = Reservation.objects.create(table=user_table,customer=customer, reserve_start= r_s,reserve_end=r_end, reserved_on=datetime.now())
        reservation.save()
        self.assertEqual(str(reservation), f'{customer.username} reserved {user_table.title}')

    def test_can_not_create_reservation_with_empty_input(self):
        self.client.post(self.register_url, self.user, format='text/html')
        username = self.user['username']
        password = self.user['password1']
        self.user_login = {'username': username, 'password': password}
        self.client.post(self.login_url, self.user_login)
        user_table = Table.objects.create(**self.table)
        user_table.save()
        response = self.client.post(self.table_to_reserve_url, self.empty_reservation_input)
        self.assertEqual(response.status_code, 302)

    def test_can_not_reserve_from_past(self):
        self.client.post(self.register_url, self.user, format='text/html')
        username = self.user['username']
        password = self.user['password1']
        self.user_login = {'username':username, 'password': password}
        self.client.post(self.login_url, self.user_login)
        user_table = Table.objects.create(**self.table)
        user_table.save()
        response = self.client.post(self.table_to_reserve_url, self.past_reservation_input)
        self.assertEqual(response.status_code, 302)

    def test_can_create_reservation_with_correct_input(self):
        self.client.post(self.register_url, self.user, format='text/html')
        username = self.user['username']
        password = self.user['password1']
        self.user_login = {'username':username, 'password': password}
        self.client.post(self.login_url, self.user_login)
        user_table = Table.objects.create(**self.table)
        user_table.save()
        response = self.client.post(self.table_to_reserve_url, self.correct_reservation_input)
        self.assertRedirects(response, self.home_url)
        self.assertEqual(response.status_code, 302)

    def test_can_not_create_reservation_with_conflicting_times(self):
        self.client.post(self.register_url, self.user, format='text/html')
        username = self.user['username']
        password = self.user['password1']
        self.user_login = {'username':username, 'password': password}
        self.client.post(self.login_url, self.user_login)
        user_table = Table.objects.create(**self.table)
        user_table.save()
        self.client.post(self.table_to_reserve_url, self.correct_reservation_input)
        response = self.client.post(self.table_to_reserve_url, self.not_available_reservation)
        self.assertEqual(response.status_code, 302)

    def test_can_show_reservation_edit_page(self):
        self.client.post(self.register_url, self.user, format='text/html')
        username = self.user['username']
        password = self.user['password1']
        self.user_login = {'username':username, 'password': password}
        self.client.post(self.login_url, self.user_login)
        user_table = Table.objects.create(**self.table)
        user_table.save()
        self.client.post(self.table_to_reserve_url, self.correct_reservation_input)
        response = self.client.get(self.reservation_to_edit)
        self.assertTemplateUsed(response, 'restaurant/reservation_edit.html')
        self.assertEqual(response.status_code, 200)

    def test_can_edit_reservation_with_correct_input(self):
        self.client.post(self.register_url, self.user, format='text/html')
        username = self.user['username']
        password = self.user['password1']
        self.user_login = {'username':username, 'password': password}
        self.client.post(self.login_url, self.user_login)
        user_table = Table.objects.create(**self.table)
        user_table.save()
        self.client.post(self.table_to_reserve_url, self.correct_reservation_input)
        response = self.client.post(self.reservation_to_edit, self.edit_correct_reservation)
        self.assertEqual(response.status_code, 302)

    def test_for_empty_or_invalid_edit_input(self):
        self.client.post(self.register_url, self.user, format='text/html')
        username = self.user['username']
        password = self.user['password1']
        self.user_login = {'username':username, 'password': password}
        self.client.post(self.login_url, self.user_login)
        user_table = Table.objects.create(**self.table)
        user_table.save()
        self.client.post(self.table_to_reserve_url, self.correct_reservation_input)
        response = self.client.post(self.reservation_to_edit, self.empty_reservation_input)
        self.assertEqual(response.status_code, 302)


    def test_can_delete_a_reservation(self):
        self.client.post(self.register_url, self.user, format='text/html')
        username = self.user['username']
        password = self.user['password1']
        self.user_login = {'username':username, 'password': password}
        self.client.post(self.login_url, self.user_login)
        user_table = Table.objects.create(**self.table)
        user_table.save()
        self.client.post(self.table_to_reserve_url, self.correct_reservation_input)
        response = self.client.delete(self.reservation_delete)
        self.assertEqual(response.status_code, 302)


class ReviewTest(BaseTest):
    def test_show_review_list_page(self):
        response = self.client.get(self.review_list_url)
        self.assertTemplateUsed(response, 'restaurant/review_list.html')
        self.assertEqual(response.status_code, 200)

    def test_should_create_review(self):
        user_table = Table.objects.create(**self.table)
        author = User.objects.create_user(username='testme', email='noreply@gmail.com', password='password')
        review = Review.objects.create(table=user_table, author=author, content='some text...')
        review.save()
        self.assertEqual(str(review), f'{review.author} reviewed {review.table.title}')


class FoodTest(BaseTest):
    def test_show_food_list_page(self):
        response = self.client.get(self.food_list_url)
        self.assertTemplateUsed(response, 'restaurant/food_list.html')
        self.assertEqual(response.status_code, 200)

    def test_should_create_food(self):
        user_food = Food.objects.create(**self.food)
        user_food.save()
        self.assertEqual(str(user_food), f"{self.food['name']}")

    def test_should_show_image(self):
        user_food = Food.objects.create(**self.food)
        user_food.save()
        self.assertEqual(user_food.image_tag(),  mark_safe('<img src="%s" height="50" width="50">' %user_food.image.url))

    def test_should_show_no_image(self):
        food = Food.objects.create(**self.food_without_image)
        food.save()
        self.assertEqual(food.image_tag(), 'No image found')


class DrinkTest(BaseTest):
    def test_show_food_list_page(self):
        response = self.client.get(self.drink_list_url)
        self.assertTemplateUsed(response, 'restaurant/drink_list.html')
        self.assertEqual(response.status_code, 200)

    def test_should_create_drink(self):
        user_drink = Drink.objects.create(**self.drink)
        user_drink.save()
        self.assertEqual(str(user_drink), f"{self.drink['name']}")

    def test_should_show_image(self):
        user_drink = Drink.objects.create(**self.drink)
        user_drink.save()
        self.assertEqual(user_drink.image_tag(),  mark_safe('<img src="%s" height="50" width="50">' %user_drink.image.url))

    def test_should_show_no_image(self):
        drink = Drink.objects.create(**self.drink_without_image)
        drink.save()
        self.assertEqual(drink.image_tag(), 'No image found')