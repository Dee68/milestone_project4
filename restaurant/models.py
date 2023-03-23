from django.db import models
from django.utils.safestring import mark_safe
from django.utils.text import slugify
from cloudinary.models import CloudinaryField
from django.contrib.auth.models import User
from django.shortcuts import reverse

# Create your models here.


class Table(models.Model):
    TABLE_TYPE = (
        ('basic', 'basic'),
        ('vip', 'vip'),
    )
    title = models.CharField(max_length=100)
    table_type = models.CharField(max_length=5, choices=TABLE_TYPE, default='basic')
    number = models.IntegerField()
    capacity = models.IntegerField(default=1)
    cost = models.DecimalField(decimal_places=2, max_digits=10, default=100.00)
    is_available = models.BooleanField(default=True)
    slug = models.SlugField(unique=True)
    image = models.ImageField(blank=True, upload_to="tables/")
    description = models.TextField(default='Book a table and  have taste of this exotic meal.')

    def image_tag(self):
        if self.image:
            return mark_safe('<img src="%s" height="50" width="50">' %self.image.url)
        return "No image found"
    image_tag.short_description = 'Image'

    def get_absolute_url(self, *args, **kwargs):
        return reverse('restaurant:table-detail', args=[self.id, self.slug])

    def get_table_review(self, *args):
        return reverse('restaurant:table-review', args=[self.slug])

    def __str__(self):
        return f'Table number {self.number} with a capacity of {self.capacity}'


class Reservation(models.Model):
    customer = models.ForeignKey(to=User, on_delete=models.CASCADE)
    table = models.ForeignKey(to=Table, on_delete=models.CASCADE)
    reserve_start = models.DateTimeField()
    reserve_end = models.DateTimeField()
    reserved_on = models.DateTimeField(auto_now_add=False, auto_now=True)

    @property
    def get_reserve_start(self):
        return self.reserve_start.strftime('%m/%d/%Y %I:%M %p')

    @property
    def get_reserve_end(self):
        return self.reserve_end.strftime('%m/%d/%Y %I:%M %p')

    def __str__(self):
        return f'{self.customer.username} reserved {self.table.title}'


class Review(models.Model):
    table = models.ForeignKey(Table, on_delete=models.CASCADE, related_name='table_review')
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    content = models.TextField()
    date_created = models.DateTimeField(auto_now_add=True)
    date_updated = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f'{self.author.username} reviewed {self.table.title}'


FOOD_TYPE = (
    ('snacks', 'Snacks'),
    ('main', 'Main'),
    ('dessert', 'Dessert')
)
DRINK_TYPE = (
    ('wines', 'Wines'),
    ('beers', 'Beers'),
    ('cocktails', 'Cocktails')
)


class Food(models.Model):
    name = models.CharField(max_length=100)
    description = models.CharField(max_length=255)
    food_type = models.CharField(max_length=7, choices=FOOD_TYPE, default='snacks')
    price = models.DecimalField(decimal_places=2, max_digits=10)
    image = models.ImageField(upload_to='foods/', blank=True)

    def image_tag(self):
        if self.image:
            return mark_safe('<img src="%s" height="50" width="50">' %self.image.url)
        return "No image found"
    image_tag.short_description = 'Image'

    def __str__(self):
        return str(self.name)


class Drink(models.Model):
    name = models.CharField(max_length=100)
    description = models.CharField(max_length=255)
    drink_type = models.CharField(max_length=9, choices=DRINK_TYPE, default='wines')
    price = models.DecimalField(decimal_places=2, max_digits=10)
    image = models.ImageField(upload_to='drinks/', blank=True)

    def image_tag(self):
        if self.image:
            return mark_safe('<img src="%s" height="50" width="50">' %self.image.url)
        return "No image found"
    image_tag.short_description = 'Image'

    def __str__(self):
        return str(self.name)
