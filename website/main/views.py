from django.contrib import messages
from django.shortcuts import render, redirect
from .models import *
from django.contrib.auth import authenticate, login, logout
from .forms import CustomUserCreationForm


def show_users(request):
    return render(request, 'index.html')


def del_users(request):
    return render(request, 'index.html')


def register(request):
    if request.method == "POST":
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            messages.success(request, "Registration successful.")
            return redirect("index")
        else:
            messages.error(request, "Unsuccessful registration. Invalid information.")
    else:
        form = CustomUserCreationForm()
    return render(request, "register.html", {"form": form})


def logout_user(request):
    logout(request)
    return render(request, 'index.html')


def show_books(request):
    return render(request, 'index.html')


def add_books(request):
    return render(request, 'index.html')


def del_books(request):
    return render(request, 'index.html')


def index(request):
    if request.method == "POST":
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return render(request, 'index.html')
        else:
            messages.error(request, "Login failed, try again!")
    else:
        return render(request, 'index.html')
    return render(request, 'index.html')



 
# add delete, update, etc, views