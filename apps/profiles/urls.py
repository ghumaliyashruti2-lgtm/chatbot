from django.contrib import admin
from django.urls import path
from apps.profiles import views
from django.conf import settings
from django.conf.urls.static import static  

app_name = "profiles"   # ✅ MUST EXIST


urlpatterns = [
    path("profile/", views.profile, name="profile"),
    path("profile/my-profile/",views.edit_profile_detail,name="my-profile"),
    path("profile/my-profile/edit-profile/",views.edit_profile_image,name="edit-profile"),
    path("profile/my-profile/delete-profile/",views.delete_profile_image,name="delete-profile"),
    path("mobile-profile/",views.mobile_profile, name="mobileprofile")
    
]

if settings.DEBUG:
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
