from django import forms
from django.contrib.auth.forms import ReadOnlyPasswordHashField, AuthenticationForm
from .models import CustomUser

class CustomUserCreationForm(forms.ModelForm):
    password1 = forms.CharField(
        label='Password',
        widget=forms.PasswordInput,
        help_text=''
    )
    password2 = forms.CharField(
        label='Password confirmation',
        widget=forms.PasswordInput,
        help_text=''
    )

    class Meta:
        model = CustomUser
        fields = ('username', 'email', 'nickname', 'profile_image')
        help_texts = {
            'username': '',
            'email': '',
            'nickname': '',
            'profile_image': '',
        }

    def clean_password2(self):
        password1 = self.cleaned_data.get("password1")
        password2 = self.cleaned_data.get("password2")
        if password1 and password2 and password1 != password2:
            raise forms.ValidationError("비밀번호가 일치하지 않습니다.")
        return password2

    def save(self, commit=True):
        user = super().save(commit=False)
        user.set_password(self.cleaned_data["password1"])
        if commit:
            user.save()
        return user

class CustomUserChangeForm(forms.ModelForm):
    password = ReadOnlyPasswordHashField(
        help_text='원하는 경우 비밀번호를 변경하세요.'
    )

    class Meta:
        model = CustomUser
        fields = ('username', 'email', 'password', 'nickname', 'profile_image', 'is_active', 'is_staff')
        help_texts = {
            'username': '사용자 이름을 입력하세요.',
            'email': '유효한 이메일 주소를 입력하세요.',
            'nickname': '닉네임을 입력하세요.',
            'profile_image': '프로필 이미지를 선택하세요.',
        }

    def clean_password(self):
        return self.initial["password"]

class CustomAuthenticationForm(AuthenticationForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.error_messages['invalid_login'] = '아이디/비밀번호를 다시 입력해주세요!'
        self.error_messages['inactive'] = '이 계정은 비활성화되었습니다.'

from django import forms
from django.contrib.auth.forms import UserChangeForm
from .models import CustomUser

class CustomUserChangeForm(UserChangeForm):
    class Meta:
        model = CustomUser
        fields = ['username', 'nickname', 'email', 'profile_image']
        widgets = {
            'username': forms.TextInput(attrs={'class': 'form-input'}),
            'nickname': forms.TextInput(attrs={'class': 'form-input'}),
            'email': forms.EmailInput(attrs={'class': 'form-input'}),
            'profile_image': forms.FileInput(attrs={'class': 'form-input--img'}),
        }