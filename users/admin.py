from django.contrib import admin

from users.models import User


@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    list_display = ('username', 'role', 'employee_number', 'first_name', 'last_name')
    search_fields = ('username',)
