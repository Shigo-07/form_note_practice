from django.contrib import admin
from .models import User
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin

# Register your models here.
@admin.register(User)
class UserAdmin(BaseUserAdmin):
    list_display = (
        'email',
        'active',
        'staff',
        'admin',
        'python_student',
    )
    list_filter = (
        'admin',
        'active',
        'python_student',
    )
    ordering = ('email',)
    filter_horizontal = ()

    add_fieldsets = (
        (None, {
            'classes':('wide',),
            'fields':('email','password1','password2')
        }),
    )

    fieldsets = (
        (None,{'fields':('email','password')}),
        ('Permissions',{'fields':('staff','admin','python_student',)}),
    )