from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.models import User
from django.contrib import messages
from django.utils.safestring import mark_safe
from django.http import JsonResponse, HttpResponseRedirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.urls import reverse, reverse_lazy
from .models import Profile
from .forms import RegisterForm, UserProfileForm, UserUpdateForm
import re

import json

# Create your views here.


def register(request):
    regex = '^[a-z0-9]+[\._]?[ a-z0-9]+[@]\w+[. ]\w{2,3}$'
    reg_form = RegisterForm()
    context = {'reg-form': reg_form}
    if request.method == 'POST':
        reg_form = RegisterForm(request.POST)
        field_vals = request.POST
        username = request.POST['username']
        email = request.POST['email']
        password1 = request.POST['password1']
        password2 = request.POST['password2']
        context = {'reg_form': reg_form, 'field_vals': field_vals}
        if len(username) == 0 or len(password1) == 0:
            messages.error(request, 'all fields are required.')
            return render(request, 'account/register.html', context, status=400)
        if len(username) < 2 or len(username) > 8:
            messages.error(request, 'username must be between 2 or 8 characters.')
            return render(request, 'account/register.html', context, status=406)
        if not username.isalnum():
            messages.error(request, 'Only alpha numeric characters allowed.')
            return render(request, 'account/register.html', context, status=400)
        if password1 != password2:
            messages.error(request, 'Passwords do not match.')
            return render(request, 'account/register.html', context, status=404)
        # if User.objects.filter(email=email).exists():
        #     messages.error(request, 'Email already taken, choose another.')
        #     return render(request, 'account/register.html', context, status=409)
        if not (re.search(regex, email)):
            messages.error(request, 'Email is invalid.')
            return render(request, 'account/register.html', context, status=400)
        if reg_form.is_valid():
            if User.objects.filter(email=email).exists():
                messages.error(request, 'Email already taken, choose another.')
                return render(request, 'account/register.html', context, status=409)
            username = reg_form.cleaned_data.get('username')
            
            user = User.objects.create_user(username=username, email=email, password=password1)
            user.set_password(password1)
            login(request, user)
            messages.success(request, f'Account successfully created, you can now log in.')
            return render(request, 'account/register.html', context)
        else:
            messages.error(request, str(reg_form.errors))
            return render(request, 'account/register.html', context)
    return render(request, 'account/register.html', context)


def signin(request):
    context = {
        'data': request.POST,
        'has_error': False
    }
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        if username and password:
            user = authenticate(username=username, password=password)
            if user:
                login(request, user)
                messages.success(request, mark_safe('Welcome ' + user.username))
                return redirect('restaurant:home')
            elif not user and not context['has_error']:
                messages.error(request, 'Invalid credentials,try again.')
                context['has_error'] = True
                return render(request, 'account/signin.html', context, status=401)
        else:
            messages.error(request, 'All fields are required.')
            context['has_error'] = True
            return render(request, 'account/signin.html', context, status=401)
    return render(request, 'account/signin.html')


def confirm_page(request):
    form = request.POST
    if request.method == 'POST':
        if form.get('yes'):
            logout(request)
            messages.success(request, 'You are now logged out.')
            return redirect('restaurant:home')
        else:
            return redirect('restaurant:home')
    return render(request, 'account/confirm.html')


def logout_page(request):
    return render(request, 'account/confirm.html')


def validate_username(request):
    data = json.loads(request.body)
    err_str = 'Username should contain only alphanumeric characters.'
    err_str1 = 'Username must be between 2 and 8 characters.'
    err_str2 = 'Sorry username already in use, choose another.'
    username = data['username']
    if not str(username).isalnum():
        return JsonResponse({'username_error': err_str}, status=400)
    if len(data['username']) <= 1 or len(data['username']) >= 9:
        return JsonResponse({'username_error': err_str1}, status=406)
    # if User.objects.filter(username=username).exists():
    #     return JsonResponse({'username_error': err_str2}, status=409)
    return JsonResponse({'username_valid': True}, status=200)


def validate_email(request):
    regex = '^[a-z0-9]+[\._]?[ a-z0-9]+[@]\w+[. ]\w{2,3}$'
    data = json.loads(request.body)
    err_str = 'Sorry,email already taken, choose another one'
    err_str1 = 'Email is invalid.'
    email = data['email']
    if User.objects.filter(email=email):
        return JsonResponse({'email_error': err_str}, status=409)
    if (re.search(regex, email)):
        return JsonResponse({'email_valid': True}, status=200)
    else:
        return JsonResponse({'email_error': err_str1}, status=400)


@login_required(login_url='account/signin')
def profile_page(request):
    user = request.user
    user_profile = get_object_or_404(Profile, user=request.user)
    context = {'user_profile': user_profile, 'user': user}
    return render(request, 'account/index.html', context)


@login_required(login_url='account/signin')
def profile_update(request):
    user_profile = Profile.objects.get(user_id=request.user.id)
    post_data = request.POST or None
    if request.method == 'POST':
        user_form = UserUpdateForm(post_data, instance=request.user)
        profile_form = UserProfileForm(post_data, request.FILES, instance=request.user.profile)
        if user_form.is_valid() and profile_form.is_valid():
            user_form.save()
            profile_form.save()
            messages.success(request, 'Your profile has been updated.')
            return HttpResponseRedirect(reverse_lazy('account:profile'))       
        messages.error(request, 'Something went wrong.')
        context={'user_form': user_form, 'profile_form': profile_form, 'user_profile': user_profile}
        return render(request, 'account/update_profile.html', context )
    user_form = UserUpdateForm(instance=request.user)
    profile_form = UserProfileForm(instance=request.user.profile)
    context = {'user_form': user_form, 'profile_form': profile_form, 'user_profile': user_profile}
    return render(request, 'account/update_profile.html', context)
