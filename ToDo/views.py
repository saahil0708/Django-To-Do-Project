from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.views.decorators.cache import never_cache

from . import models

@never_cache
@login_required(login_url='Login')
def Home(request):
    if request.method == 'POST':
        title = request.POST.get('title')
        if title:
            models.ToDoItem.objects.create(title = title, user = request.user)

        return redirect('/')

    res = models.ToDoItem.objects.filter(user = request.user).order_by('-date')

    return render(request, 'todo.html', {'res': res})

def SignUp(request):
    if request.method == 'POST':
        fnm = request.POST.get('fnm')
        email = request.POST.get('email')
        passwd = request.POST.get('passwd')

        my_User = User.objects.create_user(fnm, email, passwd)
        my_User.save()

        print(f'User Name: {fnm}, Email: {email}, Password: {passwd}')

        return redirect('Login')

    return render(request, 'signup.html')

def Login(request):
    if request.method == 'POST':
        fnm = request.POST.get('fnm')
        passwd = request.POST.get('passwd')

        print(f'User Name: {fnm}, Password: {passwd}')

        User = authenticate(request, username = fnm, password = passwd)

        if User is not None:
            login(request, User)
            print('Login Successful!')
            return redirect('/')
        else:
            # password='Invalid Credentials. Please try again!'
            # return render(request, 'login.html', {'password': password})
            pass

    return render(request, 'login.html')

def Logout(request):
    logout(request)
    return redirect('Login')

@login_required(login_url='Login')
def Edit(request, srno):
    todo = models.ToDoItem.objects.get(srno=srno, user=request.user)
    
    if request.method == 'POST':
        title = request.POST.get('title')
        if title:
            todo.title = title
            todo.save()
            return redirect('/')
            
    return render(request, 'edit.html', {'todo': todo})

@login_required(login_url='Login')
def Delete(request, srno):
    todo = models.ToDoItem.objects.get(srno=srno, user=request.user)
    todo.delete()
    return redirect('/')