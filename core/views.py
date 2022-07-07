from email import message
from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.contrib import messages
from django.contrib.auth.models import User
from .models import *
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.decorators import login_required

# Create your views here.


@login_required(login_url='signin')
def index(request):
    return render(request, 'index.html')


def signup(request):

    if request.POST:
        username = request.POST['username']
        password = request.POST['password']
        password2 = request.POST['password2']
        email = request.POST['email']

        if password == password2:
            if User.objects.filter(email=email).exists():
                messages.info(request, 'email already exists')
                return redirect('signup')
            elif User.objects.filter(username=username).exists():
                messages.info(request, 'username already exists')
                return redirect('signup')
            else:
                user = User.objects.create_user(
                    username=username, password=password, email=email)
                user.save()

                user_model = User.objects.get(username=username)
                user_profile = Profile.objects.create(
                    user=user_model, id_user=user_model.id)

                new_profile = user_profile.save()
                messages.info(request, 'user created')
                return redirect('signin')
            # return HttpResponse('Success')
        else:
            messages.info(request, 'password not matching')
            return redirect('signup')
    return render(request, 'signup.html')


def signin(request):

    if request.method == "POST":
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect('/')
        else:
            messages.info(request, 'invalid details')
            return redirect('signin')
    return render(request, 'signin.html')


@login_required(login_url='signin')
def signout(request):
    logout(request)
    return redirect('signin')


def settings(request):
    return render(request, 'settings.html')
