from django.db import models
from django.utils.safestring import mark_safe
from cloudinary.models import CloudinaryField
from django.contrib.auth.models import User

# Create your models here.


class Meal(models.Model):
    CATEGORY = (
        ('breakfast', 'breakfast'),
        ('lunch', 'lunch'),
        ('supper', 'supper')
    )
    name = models.CharField(max_length=100)
    description = models.TextField()
    price = models.DecimalField(max_digits=10, decimal_places=2)
    image = models.ImageField(blank=True, upload_to="meals/")
    #CloudinaryField('image', overwrite=True, resource_type='image')
    category = models.CharField(max_length=9, choices=CATEGORY, default='lunch')
    slug = models.SlugField(max_length=200)
    number_of_persons = models.IntegerField(default=1)


    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.title)
        super().save(*args, **kwargs)

    def image_tag(self):
        if self.image:
            return mark_safe('<img src="%s" height="50" width="50">' %self.image.url)
        return "No image found"
    image_tag.short_description = 'Image'

    def __str__(self):
        return str(self.name)


class Table(models.Model):
    TABLE_TYPE = (
        ('basic', 'basic'),
        ('vip', 'vip'),
    )
    table_type = models.CharField(max_length=5, choices=TABLE_TYPE, default='basic')
    number = models.IntegerField()
    capacity = models.IntegerField(default=1)
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
    # meal = models.ForeignKey(to=Meal, on_delete=models.CASCADE)
    cost = models.DecimalField(decimal_places=2, max_digits=10)
    reserve_date = models.DateField()
    reserve_time = models.TimeField()

    def __str__(self):
        return f'{customer.username} reserved {self.table} on {self.reserve_date} by {self.reserve_time}'
