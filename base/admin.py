from django.contrib import admin
from .models import Chat, Message, CustomUser

admin.site.register(Chat)
admin.site.register(Message)
admin.site.register(CustomUser)
