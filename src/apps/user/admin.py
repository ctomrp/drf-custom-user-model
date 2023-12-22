from .models import User
from django.contrib import admin


class UserAdmin(admin.ModelAdmin):
    list_display = ("id", "first_name", "last_name", "email")


admin.site.register(User, UserAdmin)
