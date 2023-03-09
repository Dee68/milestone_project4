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

    def __str__(self):
        return f'Table number {self.number} with a capacity of {self.capacity}'


class TableImage(models.Model):
    table = models.ForeignKey(Table, on_delete=models.CASCADE)
    images = models.ImageField(upload_to='tables/')

    def __str__(self):
        return self.table.title


class Reservation(models.Model):
    customer = models.ForeignKey(to=User, on_delete=models.CASCADE)
    table = models.ForeignKey(to=Table, on_delete=models.CASCADE)
    reserve_start = models.DateTimeField()
    reserve_end = models.DateTimeField()
    reserved_on = models.DateTimeField(auto_now_add=False, auto_now=True)

    def __str__(self):
        return f'{self.customer.username} reserved {self.table.title} on {self.reserved_on} '
