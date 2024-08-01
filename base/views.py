from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.views import PasswordChangeView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse_lazy
from .models import Chat, Message, User
from .forms import MessageForm, RegisterForm, CustomAuthenticationForm, CustomPasswordChangeForm, CreateChatForm

def chat(request):
    chats = Chat.objects.all()
    context = {"chats": chats}
    return render(request, "base/chat.html", context=context)

def chatDetails(request, chat_name, pk):
    chat_object = get_object_or_404(Chat, id=pk, name=chat_name)
    messageForm = MessageForm()
    messages = chat_object.messages.all().order_by("created")
    participants = chat_object.participants.all()
    context = {"chat": chat_object, 
               "messages": messages, 
               "form": messageForm, 
               "participants": participants}
    return render(request, "base/chat_details.html", context=context)

def sendMessage(request, pk):
    chat = get_object_or_404(Chat, id=pk)
    if request.method == "POST":
        message = Message(
            author=request.user,
            chat=chat,
            body=request.POST.get("body")
        )
        message.save()
        return redirect("chat_details", chat.name, pk)
    messages = chat.messages.all().order_by("created")
    context = {"chat": chat, "messages": messages}
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
    user = get_object_or_404(User, username=username, id=pk)
    chats = Chat.objects.filter(
        participants__id=user.id
    )
    messages = Message.objects.filter(
        author=user
    )
    context = {
        "user": user, 
        "chats": chats, 
        "messages": messages
    }
    return render(request, "base/profile.html", context=context)

def showingProfile(request, username, pk):
    user = get_object_or_404(User, username=username, id=pk)
    visitor = authenticate(id=request.user.id)
    if visitor is not None:
        login(request, visitor)
    chats = Chat.objects.filter(
        participants__id=user.id
    )
    messages = Message.objects.filter(
        author=user
    )
    context = {
        "user": user, 
        "chats": chats, 
        "messages": messages
    }
    return render(request, "base/showing_profile.html", context=context)

def createChat(request):
    if request.method == "POST":
        form = CreateChatForm(request.POST)
        if form.is_valid():
            newChat = form.save(commit=False)
            newChat.host = request.user
            newChat.save()
            return redirect("chat")
    else:
        form = CreateChatForm()
    context = {"form": form}
    return render(request, "base/create_chat.html", context=context)

def addParticipant(request, chat_name, pk):
    chat = get_object_or_404(Chat, name=chat_name, id=pk)
    
    if request.method == 'POST':
        username = request.POST.get('username')
        if username:
            participant = get_object_or_404(User, username=username)
            if participant:
                if participant in chat.participants.all():
                    messages.info(request, "This chat already has the participant!")
                else:
                    chat.participants.add(participant)
                    messages.success(request, "Participant added!")
            else:
                messages.error(request, "There is no user with this username!")
        else:
            messages.error(request, "Username cannot be empty!")

    return redirect('chat_details', chat.name, chat.id)

class CustomPasswordChangeView(LoginRequiredMixin, PasswordChangeView):
    form_class = CustomPasswordChangeForm
    template_name = 'base/change_password.html'
    success_url = reverse_lazy('change_password_success')

