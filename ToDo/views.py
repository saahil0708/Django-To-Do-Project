from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout

from . import models

def Home(request):
    if request.method == 'POST':
        title = request.POST.get('title')
        print(f'Title: {title}')

        obj = models.ToDoItem(title = title, user = request.user)
        obj.save()

        res = models.ToDoItem.objects.filter(user = request.user).order_by('-date')
        return redirect('/', {
            'res': res
        })
    res = models.ToDoItem.objects.filter(user = request.user).order_by('-date')
    return render(request, 'todo.html')

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