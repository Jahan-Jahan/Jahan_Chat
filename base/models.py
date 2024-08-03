from django.db import models
from django.contrib.auth.models import AbstractUser, Group, Permission

class CustomUser(AbstractUser):
    friends = models.ManyToManyField("self", symmetrical=True, blank=True)
    created = models.DateTimeField(auto_now_add=True)

    groups = models.ManyToManyField(
        Group,
        related_name='customuser_set', 
        blank=True,
        help_text='The groups this user belongs to. A user will get all permissions granted to each of their groups.',
        related_query_name='customuser',
    )
    user_permissions = models.ManyToManyField(
        Permission,
        related_name='customuser_set', 
        blank=True,
        help_text='Specific permissions for this user.',
        related_query_name='customuser',
    )

    class Meta:
        ordering = ["created"]

    def __str__(self):
        return self.username

class Chat(models.Model):
    name = models.CharField(max_length=50, unique=True)
    host = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name="hosted_chats")
    participants = models.ManyToManyField(CustomUser, related_name="chats")
    description = models.TextField(blank=True)
    created = models.DateTimeField(auto_now_add=True)
    status = models.CharField(max_length=10, choices=[("open", "open"), ("close", "close")], default="open")
    isDirect = models.BooleanField(default=False)

    class Meta:
        ordering = ["-created"]
        indexes = [
            models.Index(fields=["created"]),
        ]

    def __str__(self):
        return f"'{self.name}' hosted by '{self.host.username}'"

class Message(models.Model):
    author = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name="messages")
    chat = models.ForeignKey(Chat, on_delete=models.CASCADE, related_name="messages")
    body = models.TextField()
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ["created"]
        indexes = [
            models.Index(fields=["created"]),
        ]

    def __str__(self):
        return self.body[:50]

class Comment(models.Model):
    author = models.CharField(max_length=100, blank=False)
    email = models.EmailField(blank=False)
    topic = models.CharField(max_length=50, blank=True)
    body = models.TextField(max_length=500, blank=False)

    def __str__(self) -> str:
        return self.body[:50]