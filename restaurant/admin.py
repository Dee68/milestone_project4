from django.contrib import admin
from .models import Table, Reservation, Review, Food, Drink


class TableAdmin(admin.ModelAdmin):
    list_display = ['number', 'capacity', 'image_tag']
    readonly_fields = ['image_tag']
    prepopulated_fields = {'slug': ('title',)}


admin.site.register(Table, TableAdmin)
admin.site.register(Reservation)
admin.site.register(Review)
admin.site.register(Food)
admin.site.register(Drink)
