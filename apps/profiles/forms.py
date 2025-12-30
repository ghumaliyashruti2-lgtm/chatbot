from django import forms
from django.contrib.auth.models import User
from apps.profiles.models import Profile


# ==========================
# USER NAME FORM
# ==========================
class UserNameForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ["first_name", "last_name"]

        widgets = {
            "first_name": forms.TextInput(attrs={
                "class": "form-control",
                "name": "firstname",   # 🔥 MATCH VIEW
                "placeholder": "First name"
            }),
            "last_name": forms.TextInput(attrs={
                "class": "form-control",
                "name": "lastname",    # 🔥 MATCH VIEW
                "placeholder": "Last name"
            }),
        }


# ==========================
# PROFILE DETAILS FORM
# ==========================
class ProfileDetailForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = ["gender", "mobile"]

        widgets = {
            "gender": forms.Select(attrs={
                "class": "form-control",
                "name": "gender"
            }),
            "mobile": forms.TextInput(attrs={
                "class": "form-control",
                "name": "mobile",
                "placeholder": "Mobile number"
            }),
        }


# ==========================
# PROFILE IMAGE FORM
# ==========================
class ProfileImageForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = ["profile_picture"]

        widgets = {
            "profile_picture": forms.FileInput(attrs={
                "class": "form-control",
                "name": "profile_picture",
                "accept": "image/*"
            }),
        }
