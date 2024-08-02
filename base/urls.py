from django.urls import path
from . import views
from django.contrib.auth import views as auth_views


urlpatterns = [
    path("profile/<str:username><str:pk>/", views.profile, name="profile"),
    path("show-profile/<str:username><str:pk>/", views.showingProfile, name="showing_profile"),

    path("login/", views.loginPage, name="login"),
    path("register/", views.registerPage, name="register"),
    path("logout/", views.logoutPage, name="logout"),

    path("", views.chat, name="chat"),

    path("friends/", views.seeFriends, name="friends"),
    path("direct-message/<str:username>/", views.direct, name="direct"),
    path("success-send/<str:pk>/", views.sendDirectMessage, name="success_direct_send"),

    path("chat-details/<str:chat_name>-<str:pk>/", views.chatDetails, name="chat_details"),
    path("add-participant/<str:chat_name>-<str:pk>/", views.addParticipant, name="add_participant"),
    path("success-send/<str:pk>/", views.sendMessage, name="success_send"),
    
    path("change-password/", views.CustomPasswordChangeView.as_view(), name="change_password"),
    path("change-password/success/", auth_views.PasswordChangeDoneView.as_view(template_name="base/change_password_success.html"), name="change_password_success"),

    path("create-chat/", views.createChat, name="create_chat"),
    path("add-friend/<str:pk>/", views.addFriend, name="add_friend"),
]