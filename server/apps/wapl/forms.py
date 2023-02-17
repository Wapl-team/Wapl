from django import forms
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm, UserChangeForm
from .models import User
from django.contrib.auth.hashers import check_password

class SignupForm(UserCreationForm):
    class Meta:
        model = User
        fields = ['default_image', 'name', 'nickname', 'username', 'password1', 'password2']
        labels = {
			'name': '이름',		
			'nickname': '닉네임',		
			'username': '아이디',
		}

class LoginForm(AuthenticationForm):
    error_messages = {
        'invalid_login': (
            "비밀번호나 이메일이 올바르지 않습니다. 다시 확인해 주세요."
        ),
    }

    def __init__(self, *args, **kwargs):
        super(LoginForm, self).__init__(*args, **kwargs)
        self.fields['username'].label = '아이디'
        self.fields['password'].label = '비밀번호'

class EditProfileForm(UserChangeForm):
    password = None
    class Meta:
        model = User
        fields = ['name', 'nickname']

class SocialSignupForm(UserChangeForm):
    password = None
    class Meta:
        model = User
        fields = ['default_image', 'name', 'nickname']

class CheckPasswordForm(forms.Form):
    password = forms.CharField(label='비밀번호', widget=forms.PasswordInput(
        attrs={'class': 'form-control',}), 
    )
    def __init__(self, user, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.user = user

    def clean(self):
        cleaned_data = super().clean()
        password = cleaned_data.get('password')
        confirm_password = self.user.password
        
        if password:
            if not check_password(password, confirm_password):
                self.add_error('password', '비밀번호가 일치하지 않습니다.')
