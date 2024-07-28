from django.urls import path
from . import views

urlpatterns = [
    path('', views.chat, name="chat"),
    path('chat<str:pk>/', views.chatDetails, name="chat_details"),
    path('success-send<str:pk>/', views.sendMessage, name="success_send"),
]