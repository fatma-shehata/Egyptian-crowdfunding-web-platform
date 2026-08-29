from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from .models import User, RegularUser, AdminUser


@admin.register(User)
class UserAdmin(BaseUserAdmin):
    list_display = ("email", "first_name", "last_name", "mobile_phone", "is_activated", "is_staff")
    list_filter = ("is_activated", "is_staff", "country")
    search_fields = ("email", "first_name", "last_name", "mobile_phone")

    fieldsets = (
        (None, {"fields": ("email", "password")}),
        ("Personal Data", {"fields": ("first_name", "last_name", "mobile_phone", "profile_picture", "birthdate", "country")}),
        ("Permissions", {"fields": ("is_activated", "is_active", "is_staff", "is_superuser", "groups", "user_permissions")}),
    )
    add_fieldsets = (
        (None, {
            "classes": ("wide",),
            "fields": ("email", "username", "first_name", "last_name", "mobile_phone", "password1", "password2"),
        }),
    )

@admin.register(RegularUser)
class RegularUserAdmin(UserAdmin):
    list_display = ("email", "first_name", "last_name", "mobile_phone", "is_activated", "date_joined")
    list_filter = ("is_activated", "country")

    def get_queryset(self, request):
        return RegularUser.objects.get_queryset()


@admin.register(AdminUser)
class AdminUserAdmin(UserAdmin):
    list_display = ("email", "first_name", "last_name", "is_superuser", "date_joined")
    list_filter = ("is_superuser",)

    def get_queryset(self, request):
        return AdminUser.objects.get_queryset()