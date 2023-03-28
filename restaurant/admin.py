from django.contrib import admin
from rangefilter.filters import DateRangeFilter
from .models import Table, Reservation, Review, Food, Drink


class TableAdmin(admin.ModelAdmin):
    list_display = ['number', 'capacity', 'image_tag']
    readonly_fields = ['image_tag']
    prepopulated_fields = {'slug': ('title',)}


class ReservationAdmin(admin.ModelAdmin):
    list_filter = (
        'customer',
        'table',
        'reserve_start',
        'reserve_end',
        'reserve_on'
        )
    list_display = (
        'customer',
        'table',
        'reserve_start',
        'reserve_end')

    search_fields = ('customer__username',)
    list_filter = (('reserve_start', DateRangeFilter),)


class FoodAdmin(admin.ModelAdmin):
    list_display = ('name','food_type', 'image_tag',)
    readonly_fields = ['image_tag']
    search_fields = ('name', 'description',)
    list_filter = ['food_type',]


class DrinkAdmin(admin.ModelAdmin):
    list_display = ('name','drink_type', 'image_tag',)
    readonly_fields = ['image_tag']
    search_fields = ('name', 'description',)
    list_filter = ['drink_type',]


admin.site.register(Table, TableAdmin)
admin.site.register(Reservation, ReservationAdmin)
admin.site.register(Review)
admin.site.register(Food, FoodAdmin)
admin.site.register(Drink, DrinkAdmin)
