from django.shortcuts import render, redirect
from django.contrib.auth import login as auth_login, logout as auth_logout
from django.contrib.auth.decorators import login_required
from apps.author.forms import SignupForm, LoginForm


def signup(request):
    if request.user.is_authenticated:
        return redirect("chatbot")

    if request.method == "POST":
        form = SignupForm(request.POST)
        if form.is_valid():
            user = form.save()
            auth_login(request, user)
            return redirect("chatbot")
    else:
        form = SignupForm()

    return render(request, "base/signup.html", {"form": form})


def login(request):
    if request.user.is_authenticated:
        return redirect("chatbot")

    if request.method == "POST":
        form = LoginForm(request.POST)
        if form.is_valid():
            auth_login(request, form.cleaned_data["user"])
            return redirect("chatbot")
    else:
        form = LoginForm()

    return render(request, "base/login.html", {"form": form})


@login_required
def logout(request):
    auth_logout(request)
    return redirect("home")


def home(request):
    return render(request, "base/home.html")
