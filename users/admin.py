from django.contrib import admin

from users.models import User


@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    list_display = (
        'id',
        'first_name',
        'last_name',
        'email',
        'is_staff',
        'is_active',
        'is_superuser',
    )
    list_filter = ('id',)
    search_fields = ('first_name', 'last_name', 'email',)
