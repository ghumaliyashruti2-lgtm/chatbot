from django.contrib import admin
from django.urls import path
from django.conf import settings
from django.shortcuts import render
from django.conf.urls.static import static
from django.http import HttpResponse,HttpResponseRedirect
from django.shortcuts import render,redirect
from Signup.models import Signup
from Login.models import Login
from django.contrib import messages
from django.contrib.auth.hashers import check_password
from django.contrib.auth.hashers import make_password

# Simple view to render your index.html
def index(request):
    return render(request, "index.html")


def signup(request):
    if request.method == "POST":
        name = request.POST.get("signup_name")
        email = request.POST.get("signup_email")
        password = request.POST.get("signup_password")
        confirm_password = request.POST.get("signup_confirm_password")

        if not name or not email or not password or not confirm_password:
            return render(request, "signup.html", {'error': True})

        if password != confirm_password:
            return render(request,"signup.html",{'Password_not_match_error': True})
        
        if Signup.objects.filter(signup_name=name).exists():
            return render(request, "signup.html", {"user_exits_error": "Username already exists! "})

        # Email already exists
        if Signup.objects.filter(signup_email=email).exists():
            return render(request, "signup.html", {"emil_exits_error": "Email already exists!"})
        
        if Login.objects.filter(login_email=email).exists():
            return redirect("signup.html", {"already_register": "You are already Registered! Now Login please"})

        # Save signup data
        Signup.objects.create(
            signup_name=name,
            signup_email=email,
            signup_password=password,
            signup_confirm_password=confirm_password
        )

        # Automatically create login record
        Login.objects.create(
            login_email=email,
            login_password=make_password(password)  # HASHED
        )

        return render(request, "login.html")

    return render(request, "signup.html")


def login(request):
    if request.method == "POST":
        email = request.POST.get("login_email")
        password = request.POST.get("login_password")

        # Check empty fields
        if not email or not password:
            return render(request, "login.html", {'empty_error': True})

        # Check if user exists
        try:
            user = Login.objects.get(login_email=email)
        except Login.DoesNotExist:
           return render(request, "login.html", {'user_not_found': True})

        # Compare hashed password
        if not check_password(password, user.login_password):
             # WRONG PASSWORD
            return render(request, "login.html", {'password_error': True})
        else:
            # LOGIN SUCCESS
            request.session["user_id"] = user.id
            return render(request, "index.html")

    if request.session.get("user_id"):
        return render(request, "index.html", {"already_login": True})
    
    return render(request, "login.html")


