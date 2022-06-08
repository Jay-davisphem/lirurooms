from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.models import User
from django.http import HttpRequest
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import UserCreationForm
from django import forms
from django.utils import timezone
from datetime import timedelta

from .models import Message, Room
from .forms import UsernameForm


# @login_required(login_url="/login")
def home(request: HttpRequest):
    rooms = Room.objects.all()
    context = {"rooms": rooms}
    return render(request, "chat/home.html", context)


@login_required(login_url="/login")
def chatroom(request: HttpRequest, pk: int):
    room = get_object_or_404(Room, pk=pk)
    chats = room.message_set.all()

    lchats = chats.last()
    lchats = lchats.created if lchats else timezone.now()

    luser = chats.filter(owner=request.user).last()
    luser = luser.created if luser else timezone.now()
    if timezone.now() > lchats + timedelta(
        minutes=30
    ) and timezone.now() > luser + timedelta(minutes=30):
        chats.delete()
    if request.method == "POST":
        message = Message.objects.create(
            owner=request.user, room=room, content=request.POST.get("new_message")
        )
        return redirect("room", pk=room.id)
    context = {"room": room, "chats": chats}
    return render(request, "chat/chat-room.html", context)


@login_required(login_url="/login")
def create_room(request):
    data = request.POST
    if request.method == "POST":
        try:
            room = Room.objects.create(owner=request.user, name=data["room_name"])
            return redirect("room", pk=room.id)
        except:
            raise forms.ValidationError("Room already exists!")

    context = {}
    return render(request, "chat/room-form.html", context)


def login_view(request):
    page = "login"
    if request.user.is_authenticated:
        return redirect("/")
    if request.method == "POST":
        username = request.POST.get("username").lower()
        password = request.POST.get("password")

        try:
            user = User.objects.get(username=username)
        except:
            messages.error(request, "User does not exists!")
        user = authenticate(request, username=username, password=password)
        if user:
            login(request, user)
            return redirect("/")
        else:
            messages.error(request, "Username OR password is incorrect!")
    context = {"page": "login"}
    return render(request, "chat/login_register.html", context)


def register_view(request):
    page = "register"
    form = UserCreationForm()
    if request.method == "POST":
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)

            user.username = user.username.lower()
            user.save()
            login(request, user)
            return redirect("/")
        else:
            messages.error(request, "An error occured during registration")
    context = {"page": page, "form": form}
    return render(request, "chat/login_register.html", context)


def logout_view(request):
    Message.objects.filter(owner=request.user).delete()
    logout(request)
    return redirect("/")
