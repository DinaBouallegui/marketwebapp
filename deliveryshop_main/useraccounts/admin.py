from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import User

# class CustomUserAdmin(UserAdmin):
#     list_display = ('email', 'is_staff', 'is_active',)
#     list_filter = ('email', 'is_staff', 'is_active',)
#     search_fields = ('email',)
#     ordering = ('email',)
#     filter_horizontal = ()
#     fieldsets = (
#         (None, {'fields': ('email', 'password')}),
#         ('Permissions', {'fields': ('is_staff', 'is_active')}),
#     )
#     add_fieldsets = (
#         (None, {
#             'classes': ('wide',),
#             'fields': ('email', 'password1', 'password2', 'is_staff', 'is_active')}
#         ),
#     )

#registering the user model
# admin.site.register(User, CustomUserAdmin)

class CustomUserAdmin(UserAdmin):
     #making the password field non editable
     list_display = ('email', 'username', 'role','is_active','first_name','last_name')
     filter_horizontal = ()
     list_filter = ()
     fieldsets = ()
     #tuple with one element eneds a , at the end
     ordering = ('email',)
    #  list_display = ('email', 'username', 'role','is_active')
    #  list_filter = ('email', 'is_staff', 'is_active',)
    #  search_fields = ('email',)

admin.site.register(User,CustomUserAdmin)