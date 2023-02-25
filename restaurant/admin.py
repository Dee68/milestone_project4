from django.contrib import admin
from .models import Meal, Table, Reservation


# Register your models here.

admin.site.register(Meal)
admin.site.register(Table)
admin.site.register(Reservation)
