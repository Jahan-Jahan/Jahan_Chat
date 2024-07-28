from django.shortcuts import render, redirect, get_object_or_404
from .models import Chat, Message, User
from .forms import MessageForm


def chat(request):
    chats = Chat.objects.all()
    context = {"chats": chats}
    return render(request, "base/chat.html", context=context)

def chatDetails(request, pk):
    chat_object = get_object_or_404(Chat, id=pk)
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
