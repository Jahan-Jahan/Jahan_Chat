from django.urls import path
from . import views

urlpatterns = [
    path('profile/<str:username><str:pk>/', views.profile, name="profile"),

    path('login/', views.loginPage, name="login"),
    path('register/', views.registerPage, name="register"),
    path('logout/', views.logoutPage, name="logout"),

    path('', views.chat, name="chat"),
    path('chat_details/<str:chat_name>-<str:pk>/', views.chatDetails, name="chat_details"),
    path('success-send<str:pk>/', views.sendMessage, name="success_send"),

]