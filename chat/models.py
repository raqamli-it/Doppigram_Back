from django.db import models
from django.contrib.auth import get_user_model

User = get_user_model()


class Chat(models.Model):
    participants = models.ManyToManyField(User, related_name="chats")
    created = models.DateTimeField(auto_now_add=True)


class Message(models.Model):
    chat = models.ForeignKey(Chat, on_delete=models.CASCADE, related_name="messages")
    sender = models.ForeignKey(User, on_delete=models.CASCADE, related_name="sent_messages")
    content = models.TextField()
    type = models.CharField(max_length=20, default="text")
    created = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.sender} -> Chat {self.chat.id}: {self.content[:30]}"