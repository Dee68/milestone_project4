from django.contrib.auth.models import User
from django.core.exceptions import ValidationError
from .models import Profile
from django.contrib.auth.forms import UserCreationForm, UserChangeForm
from django.forms import widgets
from django import forms


class RegisterForm(UserCreationForm):
    class Meta:
        model = User
        fields = ['username', 'email', 'password1', 'password2']
 
    # def clean(self):
    #     super(UserCreationForm, self).clean()
    #     email = self.cleaned_data.get('email')
    #     if User.objects.filter(email=email).exists():
    #         raise ValidationError('Email already taken, choose another.')
    #     return self.cleaned_data
    

class UserUpdateForm(UserChangeForm):
    class Meta:
        model = User
        fields = ['username', 'email', 'first_name', 'last_name']


GENDER = (
        ('male', 'male'),
        ('female', 'female'),
    )


class UserProfileForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = ['gender', 'bio', 'avatar', 'address']
