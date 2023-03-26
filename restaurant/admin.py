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


admin.site.register(Table, TableAdmin)
admin.site.register(Reservation, ReservationAdmin)
admin.site.register(Review)
admin.site.register(Food)
admin.site.register(Drink)
