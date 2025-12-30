from django.db import models
from django.contrib.auth.models import User
import uuid


class NewChat(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    chat_id = models.CharField(max_length=100)
    user_message = models.TextField()
    ai_message = models.TextField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user.username} - {self.chat_id}"
