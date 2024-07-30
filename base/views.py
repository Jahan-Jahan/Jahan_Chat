from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import login, logout, authenticate
from .models import Chat, Message, User
from .forms import MessageForm, RegisterForm, CustomAuthenticationForm


def chat(request):
    chats = Chat.objects.all()
    context = {"chats": chats}
    return render(request, "base/chat.html", context=context)

def chatDetails(request, chat_name, pk):
    chat_object = get_object_or_404(Chat, id=pk, name=chat_name)
    messageForm = MessageForm()
    messages = chat_object.messages.all().order_by("created")
    context = {"chat": chat_object, "messages": messages, "form": messageForm}
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
        return redirect("chat_details", pk)
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
