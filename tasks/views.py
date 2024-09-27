from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth.models import User
from django.contrib.auth import login, logout, authenticate
from django.db import IntegrityError
from django.urls import reverse

#from .models import CustomUser


def home(request):
    return render(request, 'home.html')


def signup(request):
    if request.method == 'GET':
        return render(request, 'signup.html', {
            'form': UserCreationForm
        })
    else:
        print(request.POST)
        if request.POST['password1'] == request.POST['password2']:
            try:
                user = User.objects.create_user(
                    username=request.POST['username'], password=request.POST['password1'])
                user.save()
                login(request, user)
                url = reverse('user_profile', args=[user.username])
                return redirect(url)
            except IntegrityError:
                return render(request, 'signup.html', {
                    'form': UserCreationForm,
                    "error": 'Username already exists'
                })
        return render(request, 'signup.html', {
            'form': UserCreationForm,
            "error": 'Password do not match'
        })


def tasks(request):
    return render(request, 'tasks.html')


def signout(request):
    logout(request)
    return redirect('home')


def signin(request):
    if request.method == 'GET':
        return render(request, 'signin.html', {
            'form': AuthenticationForm
        })
    else:
        user = authenticate(request, username= request.POST['username'], password=request.POST['password'])
        if user is None:
            return render(request, 'signin.html', {
                'form': AuthenticationForm, 'error': 'Username or Password is incorrect'
            })
        else:
            login(request, user)
            url = reverse('user_profile', args=[user.username])
            return redirect(url)


def user_profile(request, username):
    user = get_object_or_404(User, username=username)
    return render(request, 'profile.html', {'user': user})
