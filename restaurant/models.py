from django.db import models
from django.utils.safestring import mark_safe
from cloudinary.models import CloudinaryField
from django.contrib.auth.models import User

# Create your models here.


class Table(models.Model):
    TABLE_TYPE = (
        ('basic', 'basic'),
        ('vip', 'vip'),
    )
    table_type = models.CharField(max_length=5, choices=TABLE_TYPE, default='basic')
    number = models.IntegerField()
    capacity = models.IntegerField(default=1)
    cost = models.DecimalField(decimal_places=2, max_digits=10, default=100.00)
    image = models.ImageField(blank=True, upload_to="tables/")

    def image_tag(self):
        if self.image:
            return mark_safe('<img src="%s" height="50" width="50">' %self.image.url)
        return "No image found"
    image_tag.short_description = 'Image'

    def __str__(self):
        return f'Table number {self.number} with a capacity of {self.capacity}'


class Reservation(models.Model):
    customer = models.ForeignKey(to=User, on_delete=models.CASCADE)
    table = models.ForeignKey(to=Table, on_delete=models.CASCADE)
    reserve_date = models.DateField()
    reserve_time = models.TimeField()

    def __str__(self):
        return f'{customer.username} reserved {self.table} on {self.reserve_date} by {self.reserve_time}'
