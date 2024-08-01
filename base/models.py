from django.db import models
from django.contrib.auth.models import User

class Chat(models.Model):
    name = models.CharField(max_length=50, unique=True)
    host = models.ForeignKey(User, on_delete=models.CASCADE, related_name='hosted_chats')
    participants = models.ManyToManyField(User, related_name='chats')
    description = models.TextField()
    created = models.DateTimeField(auto_now_add=True)
    status = models.CharField(max_length=10, choices=[("open", "Open"), ("close", "Close")], default="Open")

    class Meta:
        ordering = ['-created']

    def __str__(self):
        return f"'{self.name}' hosted by '{self.host.username}'"

class Message(models.Model):
    author = models.ForeignKey(User, on_delete=models.CASCADE, related_name="messages")
    chat = models.ForeignKey(Chat, on_delete=models.CASCADE, related_name='messages')
    body = models.TextField()
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['created']

    def __str__(self):
        return self.body[:50]
