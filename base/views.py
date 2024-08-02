from django.shortcuts import render, redirect, get_object_or_404
from django.db import IntegrityError, transaction
from django.db.models import Q
from django.contrib import messages
from django.contrib.auth import login, logout, authenticate, get_user_model
from django.contrib.auth.views import PasswordChangeView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.decorators import login_required
from django.urls import reverse_lazy
from .models import Chat, Message, CustomUser
from .forms import MessageForm, RegisterForm, CustomAuthenticationForm, CustomPasswordChangeForm, CreateChatForm

CustomUser = get_user_model()

def chat(request):
    chats = Chat.objects.all()
    context = {"chats": chats}
    return render(request, "base/chat.html", context=context)

@login_required(redirect_field_name="login")
def chatDetails(request, chat_name, pk):
    chat_object = Chat.objects.get(id=pk, name=chat_name)
    messageForm = MessageForm()
    messages = chat_object.messages.all().order_by("created")
    participants = chat_object.participants.all()
    context = {
        "chat": chat_object, 
        "chat_messages": messages, 
        "form": messageForm, 
        "participants": participants
        }
    return render(request, "base/chat_details.html", context=context)

def sendMessage(request, pk):
    chat = Chat.objects.get(id=pk)
    chat.participants.add(request.user)
    if request.method == "POST":
        message = Message(
            author=request.user,
            chat=chat,
            body=request.POST.get("body")
        )
        message.save()
        return redirect("chat_details", chat.name, pk)
    messages = chat.messages.all().order_by("created")
    context = {
        "chat": chat, 
        "chat_messages": messages
        }
    return render(request, "base/chat_details.html", context=context)

def registerPage(request):
    if request.method == "POST":
        form = RegisterForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get("username")
            password = form.cleaned_data.get("password1")
            user = authenticate(username=username, password=password)
            if user is not None:
                login(request, user, backend='django.contrib.auth.backends.ModelBackend')
                return redirect("chat")
            else:
                print("Authentication failed")
    else:
        form = RegisterForm()

    context = {"form": form}
    return render(request, "base/register.html", context=context)

def loginPage(request):
    if request.method == "POST":
        form = CustomAuthenticationForm(request, data=request.POST)
        if form.is_valid():
            username = form.cleaned_data.get("username")
            password = form.cleaned_data.get("password")
            user = authenticate(username=username, password=password)
            if user is not None:
                login(request, user)
                return redirect("chat")
    else:
        form = CustomAuthenticationForm()

    context = {"form": form}
    return render(request, "base/login.html", context=context)

def logoutPage(request):
    logout(request)
    return redirect("chat")

def profile(request, username, pk):
    user = CustomUser.objects.get(username=username, id=pk)
    chats = Chat.objects.filter(
        participants__id=user.id
    ).distinct()
    messages = Message.objects.filter(
        author=user
    ).distinct()
    context = {
        "user": user, 
        "chats": chats, 
        "chat_messages": messages
    }
    return render(request, "base/profile.html", context=context)

def showingProfile(request, username, pk):
    user = CustomUser.objects.get(username=username, id=pk)
    visitor = authenticate(id=request.user.id)
    if visitor is not None:
        login(request, visitor)
    chats = Chat.objects.filter(
        Q(participants__id=user.id) |
        Q(host__id=user.id)
    ).distinct()
    messages = Message.objects.filter(
        author=user
    ).distinct()
    context = {
        "user": user, 
        "chats": chats, 
        "chat_messages": messages
    }
    return render(request, "base/showing_profile_other.html", context=context)

@login_required(redirect_field_name="login")
def createChat(request):
    if request.method == "POST":
        form = CreateChatForm(request.POST)
        if form.is_valid():
            newChat = form.save(commit=False)
            newChat.host = CustomUser.objects.get(id=request.user.id)
            newChat.save()
            newChat.participants.add(newChat.host)
            return redirect("chat")
    else:
        form = CreateChatForm()
    context = {"form": form}
    return render(request, "base/create_chat.html", context=context)

def addParticipant(request, chat_name, pk):
    chat = Chat.objects.get(name=chat_name, id=pk)

    if request.method == 'POST':
        username = request.POST.get('username')
        if username:
            try:
                participant = CustomUser.objects.get(username=username)
                if participant in chat.participants.all():
                    messages.info(request, "Chat already has this participant!")
                else:
                    chat.participants.add(participant)
                    messages.success(request, "Participant added!")
            except CustomUser.DoesNotExist:
                messages.error(request, "User doesn't exist!")
        else:
            messages.error(request, "Username cannot be empty!")

    return redirect('chat_details', chat.name, chat.id)

def seeFriends(request):
    user = CustomUser.objects.get(id=request.user.id)
    friends = user.friends.all()
    context = {"friends": friends}
    return render(request, "base/friends.html", context=context)

def direct(request, username):
    user = CustomUser.objects.get(username=username)
    chat_name_1 = f"{user.username}-{request.user.username}"
    chat_name_2 = f"{request.user.username}-{user.username}"

    directChat = Chat.objects.filter(name__in=[chat_name_1, chat_name_2]).first()

    if not directChat:
        try:
            with transaction.atomic():
                directChat = Chat.objects.create(
                    name=chat_name_1,
                    host=request.user,
                    description=f"Direct chat: {chat_name_1}",
                    status="close",
                    isDirect=True
                )
        except IntegrityError:
            directChat = Chat.objects.get(name__in=[chat_name_1, chat_name_2])

    if not(user in directChat.participants.all() and request.user in directChat.participants.all()):
        directChat.participants.add(user)
        directChat.participants.add(request.user)

    messageForm = MessageForm()
    messages = directChat.messages.all().order_by("created")

    context = {
        "user": user, 
        "chat": directChat, 
        "chat_messages": messages, 
        "form": messageForm, 
    }
    return render(request, "base/direct_chat.html", context=context)
 
def sendDirectMessage(request, pk):
    chat = Chat.objects.get(id=pk)
    participants = chat.participants.all()
    if participants[0] == request.user:
        friend = participants[1]
    else:
        friend = participants[0]
    if request.method == "POST":
        message = Message(
            author=request.user,
            chat=chat,
            body=request.POST.get("body")
        )
        message.save()
        return redirect("direct", friend.username)
    messages = chat.messages.all().order_by("created")
    context = {
        "chat": chat, 
        "chat_messages": messages
        }
    return render(request, "base/direct_chat.html", context=context)

def addFriend(request, pk):
    user = CustomUser.objects.get(id=request.user.id)
    newFriend = CustomUser.objects.get(id=pk)
    if newFriend not in user.friends.all():
        user.friends.add(newFriend)
    return redirect("showing_profile", newFriend.username, pk)

class CustomPasswordChangeView(LoginRequiredMixin, PasswordChangeView):
    form_class = CustomPasswordChangeForm
    template_name = 'base/change_password.html'
    success_url = reverse_lazy('change_password_success')

