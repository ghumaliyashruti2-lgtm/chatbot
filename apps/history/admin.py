from django.contrib import admin
from apps.history.models import History
from django.contrib.auth.models import User

@admin.register(History)
class HistoryAdmin(admin.ModelAdmin):
    # Use the method names (strings) in list_display
    list_display = ('id', 'user', 'short_user_msg', 'short_ai_msg', 'created_at')
    list_filter = ('user', 'created_at')
    search_fields = ('user__username', 'user_message', 'ai_message')

    # Django >= 3.2 / 4.x / 5.x: use @admin.display for nicer metadata
    @admin.display(description='User message')
    def short_user_msg(self, obj):
        # return truncated text (change length as you want)
        return (obj.user_message[:50] + '...') if len(obj.user_message) > 50 else obj.user_message

    @admin.display(description='AI message')
    def short_ai_msg(self, obj):
        return (obj.ai_message[:50] + '...') if len(obj.ai_message) > 50 else obj.ai_message  
    
    