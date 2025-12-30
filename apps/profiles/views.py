
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.conf import settings
import os

from django.contrib.auth.models import User
from apps.profiles.models import Profile
from .forms import UserNameForm, ProfileDetailForm, ProfileImageForm

@login_required(login_url='login')
def profile(request):
    profile = Profile.objects.get(user=request.user)

    return render(request, "root/profile.html", {
        "user": request.user,
        "profile": profile,
    })
    
    
    
@login_required(login_url='login')
def edit_profile_detail(request):
    profile = Profile.objects.get(user=request.user)
    user = request.user

    if request.method == "POST":
        # 🔹 User model fields
        user.first_name = request.POST.get("firstname")
        user.last_name = request.POST.get("lastname")

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
        image_form = ProfileImageForm(
            request.POST,
            request.FILES,
            instance=profile
        )

        if image_form.is_valid():
            image_form.save()

        return render(request, "base/edit-profile.html", {
            "profile": profile,
            "saved": True
        })

    image_form = ProfileImageForm(instance=profile)

    return render(request, "base/edit-profile.html", {
        "profile": profile,
        "image_form": image_form
    })


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
        profile_form = ProfileDetailForm(request.POST, instance=profile)

        if profile_form.is_valid():
            profile_form.save()
            return redirect("profiles:my-profile")

    profile_form = ProfileDetailForm(instance=profile)

    return render(request, "root/mobile-profile.html", {
        "profile": profile,
        "profile_form": profile_form
    })
