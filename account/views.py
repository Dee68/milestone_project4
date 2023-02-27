from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from django.contrib import messages
from django.utils.safestring import mark_safe
from django.http import JsonResponse, HttpResponseRedirect
from django.core.validators import validate_email
from django.contrib.auth import authenticate, login, logout
from django.urls import reverse
from .forms import RegisterForm
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
        fname = request.POST['firstname']
        lname = request.POST['lastname']
        email = request.POST['email']
        passw1 = request.POST['password1']
        passw2 = request.POST['password2']
        context = {'reg_form': reg_form, 'field_vals': field_vals}
        if len(username) == 0 or len(fname) == 0 or len(lname) == 0 or len(passw1) == 0:
            messages.error(request, 'all fields are required.')
            return render(request, 'account/register.html', context, status=400)
        if len(username) < 2 or len(username) > 8:
            messages.error(request, 'username must be between 2 or 8 characters.')
            return render(request, 'account/register.html', context, status=400)
        if not username.isalnum() or not fname.isalnum() or not lname.isalnum():
            messages.error(request, 'Only alpha numeric characters allowed.')
            return render(request, 'account/register.html', context, status=400)
        if len(passw1) == 0 or len(passw2) == 0:
            messages.error(request, 'All fields are required.')
            return render(request, 'account/register.html', context, status=400)
        if passw1 != passw2:
            messages.error(request, 'Passwords do not match.')
            return render(request, 'account/register.html', context, status=404)
        if User.objects.filter(username=username).exists():
            messages.error(request, 'Username already taken, choose another.')
            return render(request, 'account/register.html', context, status=409)
        if User.objects.filter(email=email).exists():
            messages.error(request, 'Email already taken, choose another.')
            return render(request, 'account/register.html', context, status=409)
        if not (re.search(regex, email)):
            messages.error(request, 'Email is invalid.')
            return render(request, 'account/register.html', context, status=400)
        if reg_form.is_valid():
            user = User.objects.create_user(username=username, first_name=fname, last_name=lname, email=email, password=passw1)
            user.set_password(passw1)
            user.save()
            messages.success(request, 'Account successfully created, you can now log in.')
            response = redirect('account:signin')
            return response
        else:
            return render(request, 'account/register.html', context)
    return render(request, 'account/register.html', context)


def signin(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        if username and password:
            user = authenticate(username=username, password=password)
            if user:
                login(request, user)
                messages.success(request, mark_safe('Welcome ' + user.username))
                return redirect('restaurant:home')
            else:
                messages.error(request, 'Invalid credentials,try again.')
                return render(request, 'account/signin.html')
        else:
            messages.error(request, 'All fields are required.')
            return render(request, 'account/signin.html')
    return render(request, 'account/signin.html')


def confirm_page(request):
    form = request.POST
    if request.method == 'POST':
        if form.get('yes'):
            logout(request)
            messages.success(request, 'You are now logged out.')
            return redirect('restaurant:home')
        else:
            return render(request, 'restaurant/index.html')
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
    if User.objects.filter(username=username).exists():
        return JsonResponse({'username_error': err_str2}, status=409)
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
