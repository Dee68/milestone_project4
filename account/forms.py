# Imports
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
# 3rd party:
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError
from django.contrib.auth.forms import (
                                        UserCreationForm,
                                        UserChangeForm,
                                        PasswordChangeForm
                                        )
from django.forms import widgets
from django import forms
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
# Internal:
from .models import Profile
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~


class RegisterForm(UserCreationForm):
    class Meta:
        model = User
        fields = ['username', 'email', 'password1', 'password2']


class UserUpdateForm(UserChangeForm):
    first_name = forms.CharField(required=False)
    last_name = forms.CharField(required=False)

    class Meta:
        model = User
        fields = ['username', 'email', 'first_name', 'last_name']


class UserProfileForm(forms.ModelForm):
    GENDER = (
        ('male', 'male'),
        ('female', 'female'),
    )
    bio = forms.CharField(required=False)
    address = forms.CharField(required=False)
    avatar = forms.ImageField(required=False)

    class Meta:
        model = Profile
        fields = ['gender', 'bio', 'avatar', 'address']


class ChangePasswordForm(PasswordChangeForm):
    class Meta:
        model = User
        fields = ['old_password', 'new_password1', 'new_password2']
        labels = {
            'old_password': 'Old Password',
            'new_password1': 'New Password',
            'new_password2': 'Confirm Password'
        }
        widgets = {
            'old_password': forms.PasswordInput(
                    attrs={
                        'class': 'form-control',
                        'autocomplete': True,
                        'required': 'required'
                        }
                        ),
            'new_password1': forms.PasswordInput(
                    attrs={
                        'class': 'form-control',
                        'required': 'required'
                        }
                        ),
            'new_password2': forms.PasswordInput(
                    attrs={
                        'class': 'form-control',
                        'required': 'required'
                        }
                        )
        }
