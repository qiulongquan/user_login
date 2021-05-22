from django import forms
from django.contrib.auth.models import User
from captcha.fields import CaptchaField
import re


class LoginForm(forms.Form):
    username = forms.CharField(label='用户名:',
                               max_length=150,)
    password = forms.CharField(label='登录密码:', widget=forms.PasswordInput)
    captcha = CaptchaField(label='验证码')

    def email_check(self, email):
        pattern = re.compile(r"\"?([-a-zA-Z0-9.'?{}]+@\w+\.\w+)\"?")
        return re.match(pattern, email)

    # use clean methods to define custom validation rules
    # 用户输入的用户名或者Email查看是否存在，不存在返回错误信息
    def clean_username(self):
        username = self.cleaned_data.get('username')
        if self.email_check(username):
            filter_result = User.objects.filter(email__exact=username)
            if not filter_result:
                raise forms.ValidationError("该Email没有注册，请先联系管理员注册")
        else:
            filter_result = User.objects.filter(username__exact=username)
            if not filter_result:
                raise forms.ValidationError("该用户不存在，请先联系管理员注册")
        return username


class ProfileUpdateForm(forms.Form):
    username = forms.CharField(label='用户名', max_length=150, required=True)
    email = forms.EmailField(label='Email')
    org = forms.CharField(label='公司名', max_length=128)
    telephone = forms.CharField(label='联系电话',
                                max_length=50)


class PwdChangeForm(forms.Form):
    old_password = forms.CharField(label='旧密码', widget=forms.PasswordInput)

    password1 = forms.CharField(label='新密码', widget=forms.PasswordInput)
    password2 = forms.CharField(label='新密码确认', widget=forms.PasswordInput)

    # use clean methods to define custom validation rules

    def clean_password1(self):
        password1 = self.cleaned_data.get('password1')

        if len(password1) < 6:
            raise forms.ValidationError("密码长度必须大于6位")
        elif len(password1) > 20:
            raise forms.ValidationError("密码长度不能大于20位")

        return password1

    def clean_password2(self):
        password1 = self.cleaned_data.get('password1')
        password2 = self.cleaned_data.get('password2')

        if password1 and password2 and password1 != password2:
            raise forms.ValidationError("2次新密码不一致，请重新输入新密码")

        return password2
