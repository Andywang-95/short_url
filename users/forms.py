from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import get_user_model
import re

User = get_user_model()

class CustomUserCreationForm(UserCreationForm):
    error_messages = {
        'password_mismatch': "兩次輸入的密碼不一致",
    }
    
    class Meta:
        model = User
        fields = ['email']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['email'].widget.attrs.update({
            'placeholder': '請輸入 Email',
            'class': 'form-control',
        })
        self.fields['email'].error_messages = {
            'invalid': "Email 格式不正確",
            'required': "請輸入 Email",
        }
        self.fields['password1'].widget.attrs.update({
            'placeholder': '請輸入密碼',
            'class': 'form-control',
        })
        self.fields['password2'].widget.attrs.update({
            'placeholder': '請再次輸入密碼',
            'class': 'form-control',
        })

    def clean_email(self):
        email = self.cleaned_data.get('email')
        if User.objects.filter(email=email).exists():
            raise forms.ValidationError("此 Email 已被註冊")
        return email

    def clean_password1(self):
        password = self.cleaned_data.get('password1')
        if not password:
            raise forms.ValidationError("請輸入密碼")
        elif len(password) < 8:
            raise forms.ValidationError("密碼長度需至少 8 碼")
        elif not (re.search(r'[A-Za-z]', password) and re.search(r'\d', password)):
            raise forms.ValidationError("密碼需同時包含至少一個英文字母與一個數字")
        return password

    def clean(self):
        cleaned_data = super().clean()
        password1 = cleaned_data.get('password1')
        password2 = cleaned_data.get('password2')

        if password1 and password2 and password1 != password2:
            self.add_error("password2", self.error_messages['password_mismatch'])
        return cleaned_data
