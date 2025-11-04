from django.contrib import admin
from django.contrib.auth.models import User, Group
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin, GroupAdmin as BaseGroupAdmin
from .models import UserProfile

# Unregister the default User and Group admin
admin.site.unregister(User)
admin.site.unregister(Group)

# Inline for UserProfile
class UserProfileInline(admin.StackedInline):
    model = UserProfile
    can_delete = False
    verbose_name_plural = 'Profile'
    fk_name = 'user'

#  Custom User Admin
@admin.register(User)
class CustomUserAdmin(BaseUserAdmin):
    list_display = ('username', 'email', 'phone_display', 'is_staff', 'is_superuser', 'is_active')
    search_fields = ('username', 'email', 'userprofile__phone')
    inlines = (UserProfileInline,)

    def phone_display(self, obj):
        # Access phone from related UserProfile
        return obj.userprofile.phone if hasattr(obj, 'userprofile') else ''
    phone_display.short_description = 'Phone'

    def has_add_permission(self, request):
        return False  #  Disable Add user manually through admin

    def has_change_permission(self, request, obj=None):
        return True  #  Allow editing users

    def has_delete_permission(self, request, obj=None):
        return True  #  Allow admin to delete users

# Custom Group Admin (Read-only)
@admin.register(Group)
class ReadOnlyGroupAdmin(BaseGroupAdmin):
    def has_add_permission(self, request):
        return False

    def has_change_permission(self, request, obj=None):
        return False

    def has_delete_permission(self, request, obj=None):
        return False