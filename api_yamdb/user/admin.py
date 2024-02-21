from django.contrib import admin
from django.contrib.auth.admin import UserAdmin

from user.models import User

ADDITIONAL_USER_FIELDS = (
    (None, {'fields': ('bio', 'role',)}),
)


class UserAdmin(UserAdmin):
    model = User
    list_display = ('username', 'email', 'bio', 'role',)
    list_editable = ('role',)

    add_fieldsets = UserAdmin.add_fieldsets + ADDITIONAL_USER_FIELDS
    fieldsets = UserAdmin.fieldsets + ADDITIONAL_USER_FIELDS


admin.site.register(User, UserAdmin)
