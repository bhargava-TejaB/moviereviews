from django.shortcuts import render, redirect
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from .forms import UserCreateForm
from django.contrib.auth.models import User
from django.contrib.auth import login, logout, authenticate
from django.db import IntegrityError
from django.contrib.auth.decorators import login_required

def signup(request):
    if request.method == "GET":
        return render(request,'accounts/signup.html',{'form': UserCreateForm, 'error': None})
    else:
        print(request.POST['password1'], request.POST['password2'],request.POST['password1'] == request.POST['password2'])
        if request.POST['password1'] == request.POST['password2']:
            try:
                user = User.objects.create_user(request.POST['username'],password=request.POST['password1'])
                user.save()
                login(request,user)
                return redirect('home')
            except IntegrityError:
                return render(request, 'accounts/signup.html',{'form': UserCreateForm,'error': "Username already Exixts !"})
        else:
            return render(request, 'accounts/signup.html',{'form': UserCreateForm,'error': "Passwords DO not match!"})
@login_required
def logoutt(request):
    logout(request)
    return redirect('home')

def loginn(request):
    if request.method == "GET":
        return render(request, 'accounts/login.html',{'form': AuthenticationForm})
    else:
        user = authenticate(request, username=request.POST['username'],password=request.POST['password'])
        if not user:
            return render(request, 'accounts/login.html', {'form': AuthenticationForm, 'error': 'Username and Password do not match!'})
        else:
            login(request,user)
            return redirect('home')

        