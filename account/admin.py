from django.contrib import admin
from .models import Profile

# Register your models here.


class ProfileAdmin(admin.ModelAdmin):
    list_display = ['user', 'gender', 'image_tag', 'address']
    readonly_fields = ['image_tag']


admin.site.register(Profile, ProfileAdmin)
