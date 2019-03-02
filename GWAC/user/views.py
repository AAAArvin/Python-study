from django.shortcuts import render, redirect
from django.urls import reverse
from user.forms import *
from django.contrib import auth


# Create your views here.

#登录函数
def login(request):
    if request.method == 'POST':
        login_form = LoginForm(request.POST)
        if login_form.is_valid():
            user = login_form.cleaned_data['user']
            auth.login(request, user)
            #登录返回主页，需修改
            return redirect(request.GET.get('from', reverse('home')))
    else:
        login_form = LoginForm()
    context = {}
    context['login_form'] = login_form
    return render(request, 'login.html', context)

#注销函数
def logout(request):
    auth.logout(request)
    return redirect(request.GET.get('from', reverse('home')))


def profiles(request):
    context = {}
    return render(request, 'profiles.html', context)

def bind_email(request):
    pass