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

                user_login = authenticate(username=username, password=password)
                login(request, user_login)

                user_model = User.objects.get(username=username)
                user_profile = Profile.objects.create(
                    user=user_model, id_user=user_model.id)

                new_profile = user_profile.save()
                messages.info(request, 'user created')
                return redirect('settings  ')
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


@login_required(login_url='signin')
def settings(request):
    user_profile = Profile.objects.get(user=request.user)

    if request.method == "POST":
        print(request.FILES)
        if request.FILES.get('image') == None:
            image = user_profile.profileimg
            location = request.POST['location']
            bio = request.POST['bio']

            user_profile.location = location
            user_profile.bio = bio
            user_profile.profileimg = image
            # print(image)
            user_profile.save()
            messages.info(request, 'profile updated')

        if request.FILES.get('image') != None:
            image = request.FILES.get('image')
            location = request.POST['location']
            bio = request.POST['bio']

            user_profile.location = location
            user_profile.bio = bio
            user_profile.profileimg = image

            # print(image)
            user_profile.save()
        return redirect('settings')

    context = {
        'user_profile': user_profile
    }
    return render(request, 'setting.html', context)
