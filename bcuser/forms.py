from django import forms
from django.contrib.auth.hashers import check_password
from .models import Bcuser

class RegisterForm(forms.Form):
    email=forms.EmailField(
        error_messages={'required' : '이메일을 입력해주세요.'},
        max_length=64, label='이메일'
    )
    password = forms.CharField(
        error_messages={'required' : '비밀번호를 입력해주세요.'},
        widget=forms.PasswordInput, label='비밀번호'
    )
    nickname = forms.CharField(
        error_messages={'required' : '닉네임을 입력해주세요.'},
        widget=forms.PasswordInput, label='닉네임'
    )
    re_password = forms.CharField(
        error_messages={'required' : '비밀번호를 입력해주세요.'},
        widget=forms.PasswordInput, label='비밀번호'
    )
    
    def clean(self):
        cleaned_data = super().clean()
        email=cleaned_data.get('email')
        password=cleaned_data.get('password')
        re_password=cleaned_data.get('re_password')
        nickname=cleaned_data.get('nickname')
        
        #password, re_password가 있다면
        #password와 re_password비번이 일치하지 않을경우 
        
        if password and re_password:
            if password != re_password:
                self.add_error('password','비밀번호가 틀렸습니다')
                self.add_error('re_password','비밀번호가 틀렸습니다')

class LoginForm(forms.Form):
    email=forms.EmailField(
        error_messages={'required' : '이메일을 입력해주세요.'},
        max_length=64, label='이메일'
    )
    password = forms.CharField(
        error_messages={'required' : '비밀번호를 입력해주세요.'},
        widget=forms.PasswordInput, label='비밀번호'
    )
    
    def clean(self):
        cleaned_data = super().clean()
        email=cleaned_data.get('email')
        password=cleaned_data.get('password')

        if email and password :
            try:
                bcuser = Bcuser.objects.get(email=email)
            except Bcuser.DoesNotExist:
                self.add_error("email", "존재하지 않는 아이디입니다.")
                return

            if not check_password(password, bcuser.password):
                self.add_error("password", "비밀번호가 일치하지 않습니다.")