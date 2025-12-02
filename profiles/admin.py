from django.contrib import admin
from django.contrib.auth.models import User
from django.contrib.auth.admin import UserAdmin

from .models import Profile
from django.utils.html import mark_safe


class ProfileInline(admin.StackedInline):
    model = Profile
    can_delete = False
    verbose_name_plural = "Profile"
    fk_name = "user"


class CustomUserAdmin(UserAdmin):
    inlines = (ProfileInline,)

    # Add Profile fields in User list
    list_display = (
        "username",
        "email",
        "get_mobile",
        "get_gender",
        "get_profile_image",
        "is_staff",
    )
    list_select_related = ("profile",)

    def get_mobile(self, obj):
        return obj.profile.mobile if hasattr(obj, "profile") else "-"
    get_mobile.short_description = "Mobile"

    def get_gender(self, obj):
        return obj.profile.gender if hasattr(obj, "profile") else "-"
    get_gender.short_description = "Gender"

    def get_profile_image(self, obj):
        if hasattr(obj, "profile") and obj.profile.profile_picture:
            return mark_safe(
                f"<img src='{obj.profile.profile_picture.url}' width='40' height='40' style='border-radius:50%;'/>"
            )
        return "No Image"
    get_profile_image.short_description = "Image"


# Very Important
admin.site.unregister(User)
admin.site.register(User, CustomUserAdmin)
