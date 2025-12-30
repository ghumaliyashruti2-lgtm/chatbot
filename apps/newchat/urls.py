from django.contrib import admin
from django.urls import path
from apps.newchat import views
from django.conf import settings
from django.conf.urls.static import static  

urlpatterns = [
    path("chatbot/", views.new_chatbot,name="chatbot"),
]

if settings.DEBUG:
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

