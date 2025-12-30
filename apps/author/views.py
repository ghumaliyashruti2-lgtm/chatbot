from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, logout as auth_logout
from django.contrib.auth import login as auth_login
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from apps.newchat.models import NewChat

# ----------------------------
# AUTH
# ----------------------------

def signup(request):
    if request.user.is_authenticated:
        return redirect("chatbot")

    if request.method == "POST":
        name = request.POST.get("signup_name")
        email = request.POST.get("signup_email")
        password = request.POST.get("signup_password")
        confirm_password = request.POST.get("signup_confirm_password")

        if not name or not email or not password or not confirm_password:
            return render(request, "base/signup.html", {"error": True})

        if password != confirm_password:
            return render(request, "base/signup.html", {"password_not_match_error": True})

        if User.objects.filter(username=email).exists():
            return render(request, "base/signup.html", {"user_exits_error": "Username already exists!"})

        if User.objects.filter(email=email).exists():
            return render(request, "base/signup.html", {"email_exits_error": "Email already exists!"})
        
        parts = name.strip().split()
        first_name = parts[0]
        last_name = " ".join(parts[1:]) if len(parts) > 1 else ""
        
        user = User.objects.create_user(
            username=email,
            email=email,
            password=password,
            first_name=first_name,
            last_name=last_name
        )
        user.is_staff = True
        user.save()

        auth_login(request, user)   # ✅ FIXED
        return redirect("login")

    return render(request, "base/signup.html")


def login(request):
    if request.method == "POST":
        email = request.POST.get("login_email")
        password = request.POST.get("login_password")

        if not email or not password:
            return render(request, "base/login.html", {"empty_error": True})

        try:
            user_obj = User.objects.get(email=email)
        except User.DoesNotExist:
            return render(request, "base/login.html", {"email_invalid": True})

        user = authenticate(
            request,
            username=user_obj.email,
            password=password
        )

        if user is None:
            return render(request, "base/login.html", {"password_invalid": True})

        auth_login(request, user)   # ✅ FIXED

        next_url = request.GET.get("next")
        return redirect(next_url if next_url else "chatbot")

    return render(request, "base/login.html")


@login_required
def logout(request):
    auth_logout(request)
    return redirect("home")


def home(request):
    return render(request, "base/home.html")
