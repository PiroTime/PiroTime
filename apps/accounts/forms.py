from django import forms
from django.contrib.auth.forms import ReadOnlyPasswordHashField, UserChangeForm, AuthenticationForm
from django.contrib.auth.forms import ReadOnlyPasswordHashField, AuthenticationForm, UserChangeForm
from .models import CustomUser

# 회원가입 폼
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
    cohort = forms.IntegerField(
        label='Cohort',
        help_text='몇기인지 입력하세요.'
    )

    class Meta:
        model = CustomUser
        fields = ('username', 'email', 'nickname', 'profile_image', 'cohort')  # 소개 필드 제외
        help_texts = {
            'username': '',
            'email': '',
            'nickname': '',
            'profile_image': '',
            'cohort': '',
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
        user.cohort = self.cleaned_data.get("cohort")  # cohort 필드를 저장
        if commit:
            user.save()
        return user

# 프로필 수정 폼
class CustomUserChangeForm(UserChangeForm):
    password = ReadOnlyPasswordHashField(
        help_text='원하는 경우 비밀번호를 변경하세요.'
    )

    class Meta:
        model = CustomUser
        fields = ['username', 'email', 'password', 'nickname', 'profile_image', 'is_active', 'cohort', 'is_staff', 'intro']  # 소개 필드 포함
        help_texts = {
            'username': '사용자 이름을 입력하세요.',
            'email': '유효한 이메일 주소를 입력하세요.',
            'nickname': '닉네임을 입력하세요.',
            'profile_image': '프로필 이미지를 선택하세요.',
            'cohort': '몇기인지 입력하세요.',
        }
        widgets = {
            'username': forms.TextInput(attrs={'class': 'form-input'}),
            'nickname': forms.TextInput(attrs={'class': 'form-input'}),
            'email': forms.EmailInput(attrs={'class': 'form-input'}),
            'profile_image': forms.FileInput(attrs={'class': 'form-input--img'}),
            'cohort': forms.NumberInput(attrs={'class': 'form-input'}),
        }

    def clean_password(self):
        return self.initial["password"]

    def save(self, commit=True):
        user = super().save(commit=False)
        user.cohort = self.cleaned_data.get("cohort")  # cohort 필드를 저장
        if commit:
            user.save()
        return user

# 로그인 폼
class CustomAuthenticationForm(AuthenticationForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.error_messages['invalid_login'] = '아이디/비밀번호를 다시 입력해주세요!'
        self.error_messages['inactive'] = '이 계정은 비활성화되었습니다.'
        self.error_messages['inactive'] = '이 계정은 비활성화되었습니다.'
