from django.shortcuts import render, get_object_or_404
from .MyForms import LoginForm, ProfileUpdateForm, PwdChangeForm
from .models import UserProfile
from django.contrib.auth.models import User
from django.http import HttpResponseRedirect
from django.contrib import auth
from django.urls import reverse
from django.contrib.auth.decorators import login_required


@login_required
def profile(request, pk):
    user = get_object_or_404(User, pk=pk)
    try:
        userprofile = get_object_or_404(UserProfile, user=user)
    except Exception:
        userprofile = None
    return render(request, 'login/profile.html', {
        'user': user,
        'userprofile': userprofile,
    })


@login_required
def profile_update(request, pk):
    user = get_object_or_404(User, pk=pk)
    try:
        user_profile = get_object_or_404(UserProfile, user=user)
    except Exception:
        user_profile = UserProfile()
        user_profile.org = ''
        user_profile.telephone = ''

    if request.method == 'POST':
        form = ProfileUpdateForm(request.POST)

        if form.is_valid():
            user.username = form.cleaned_data['username']
            user.email = form.cleaned_data['email']
            user.save()

            user_profile.org = form.cleaned_data['org']
            user_profile.telephone = form.cleaned_data['telephone']
            user_profile.user_id = user.id
            user_profile.save()

            return HttpResponseRedirect(
                reverse('login:profile', args=[user.id]))
    else:
        default_data = {
            'username': user.username,
            'email': user.email,
            'org': user_profile.org,
            'telephone': user_profile.telephone,
        }
        form = ProfileUpdateForm(default_data)
    return render(request, 'login/profile_update.html', {
        'form': form,
        'user': user
    })


def login(request):
    if request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']

            user = auth.authenticate(username=username, password=password)

            if user is not None and user.is_active:
                auth.login(request, user)
                return HttpResponseRedirect("/index/")
            else:
                # 登录失败
                return render(request, 'login/login.html', {
                    'form': form,
                    'message': "用户名或密码错误，请再次输入正确的用户名密码"
                })
    else:
        form = LoginForm()

    return render(request, 'login/login.html', {'form': form})


@login_required
def logout(request):
    auth.logout(request)
    return HttpResponseRedirect("/login/")


@login_required
def pwd_change(request, pk):
    user = get_object_or_404(User, pk=pk)

    if request.method == "POST":
        form = PwdChangeForm(request.POST)

        if form.is_valid():
            password = form.cleaned_data['old_password']
            username = user.username

            user = auth.authenticate(username=username, password=password)

            if user is not None and user.is_active:
                new_password = form.cleaned_data['password2']
                user.set_password(new_password)
                user.save()
                return HttpResponseRedirect('/login/')

            else:
                return render(
                    request, 'login/pwd_change.html', {
                        'form': form,
                        'user': user,
                        'message': '旧密码不正确，请重新输入旧密码'
                    })
    else:
        form = PwdChangeForm()

    return render(request, 'login/pwd_change.html', {
        'form': form,
        'user': user
    })
