from django.shortcuts import render, redirect
from apps.profiles.models import Profile
from django.conf import settings
import os
from django.contrib.auth.decorators import login_required


@login_required(login_url='login')
def profile(request):
    profile = Profile.objects.get(user=request.user)
    return render(request, "root/profile.html", {
        "name": request.user.username,
        "email": request.user.email,
        "profile": profile,
    })


@login_required(login_url='login')
def edit_profile_detail(request):
    profile = Profile.objects.get(user=request.user)
    user = request.user

    if request.method == "POST":
        # 🔹 User model fields
        user.username = request.POST.get("username")
        user.email = request.POST.get("email")

        # 🔹 Profile model fields
        profile.gender = request.POST.get("gender")
        profile.mobile = request.POST.get("mobile")

        user.save()
        profile.save()

        return redirect("profiles:my-profile")

    return render(request, "root/my-profile.html", {
        "profile": profile,
        "user": user
    })

@login_required(login_url='login')
def edit_profile_image(request):
    profile, _ = Profile.objects.get_or_create(user=request.user)

    if request.method == "POST":
        if request.FILES.get("profile_picture"):
            profile.profile_picture = request.FILES["profile_picture"]
            profile.save()

        # IMPORTANT: render page with flag instead of redirect
        return render(request, "base/edit-profile.html", {
            "profile": profile,
            "saved": True
        })

    return render(request, "base/edit-profile.html", {"profile": profile})



@login_required(login_url='login')
def delete_profile_image(request):
    profile = Profile.objects.get(user=request.user)

    if request.method == "POST":
        delete_flag = request.POST.get("delete_flag")

        if delete_flag == "1":
            if profile.profile_picture and profile.profile_picture.name != "default/user_img.png":
                image_path = os.path.join(settings.MEDIA_ROOT, profile.profile_picture.name)
                if os.path.exists(image_path):
                    os.remove(image_path)

            profile.profile_picture = "default/user_img.png"
            profile.save()

        
        return render(request, "base/delete-profile.html", {
            "profile": profile,
            "closed": True
        })

    return render(request, "base/delete-profile.html", {
        "profile": profile
    })
    

@login_required(login_url='login')
def mobile_profile(request):
    profile = Profile.objects.get(user=request.user)

    if request.method == "POST":
        profile.gender = request.POST.get("gender")
        profile.mobile = request.POST.get("mobile")
        profile.save()
        return redirect("profiles:my-profile")

    return render(request, "root/mobile-profile.html", {"profile": profile})
