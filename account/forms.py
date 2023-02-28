from django.contrib.auth.models import User
from .models import Profile
from django.contrib.auth.forms import UserCreationForm, UserChangeForm, PasswordChangeForm
from django.forms import widgets
from django import forms


class RegisterForm(UserCreationForm):
    class Meta:
        model = User
        fields = ['username', 'first_name', 'last_name', 'email', 'password1', 'password2']


class UserUpdateForm(UserChangeForm):
    class Meta:
        model = User
        fields = ['username', 'email', 'first_name', 'last_name']   
        widgets = {
        'username':forms.TextInput(attrs={'class':'form-control','placeholder':'UserName'}),
        'first_name':forms.TextInput(attrs={'class':'form-control','placeholder':'First Name'}),
        'last_name':forms.TextInput(attrs={'class':'form-control','placeholder':'Last Name'}),
        'email':forms.EmailInput(attrs={'class':'form-control','placeholder':'Email.'}),
       
    }


class ChangePasswordForm(PasswordChangeForm):
    class Meta:
        model = User
        fields = ['old_password','new_password1', 'new_password2'] 
        labels = {
            'old_password':'Old Password',
            'new_password1':'New Password',
            'new_password2':'Confirm Password'
        }
        widgets = {
            'old_password':forms.PasswordInput(attrs={'class':'form-control','autocomplete':True,'required':'required'}),
            'new_password1':forms.PasswordInput(attrs={'class':'form-control', 'required':'required'}),
            'new_password2':forms.PasswordInput(attrs={'class':'form-control','required':'required'})
        }  


GENDER = (
        ('male', 'male'),
        ('female', 'female'),
    )


class UserProfileForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = ['gender','bio','avatar','address']
        widgets = {
        'gender': forms.Select(attrs={'class':'form-control','placeholder':'your gender.'}, choices=GENDER),
        'bio': forms.Textarea(attrs={'class':'form-control','placeholder':'your address here.'}),
         'avatar': forms.FileInput(attrs={'class':'form-control','placeholder':'upload your avatar'}),
        'address': forms.TextInput(attrs={'class':'form-control','placeholder':'your address'}),
         } 
