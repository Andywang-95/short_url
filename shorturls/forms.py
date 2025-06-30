from django import forms
from django.forms import ModelForm
from .models import ShortURL
import string, random, re

# 預期的資料量不會太大，所以預設使用6碼
def generate_code(length=6):
    chars = string.ascii_letters + string.digits
    while True:
        code = ''.join(random.choices(chars, k=length))
        if any(c.isdigit() for c in code) and any(c.isalpha() for c in code):
            return code

class ShortURLForm(ModelForm):
    short_url = forms.CharField(required=False)
    class Meta:
        model = ShortURL
        fields = ['url', 'short_url', 'is_active', 'password', 'remarks']
        widgets = {
            'url': forms.URLInput(attrs={'class': 'form-control'}),
            'short_url': forms.TextInput(attrs={'class': 'form-control'}),
            'is_active': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
            'password': forms.PasswordInput(attrs={'class': 'form-control'}),
            'remarks': forms.Textarea(attrs={'class': 'form-control'}),
        }
        
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        if self.instance.pk:
            self.fields['url'].widget.attrs['readonly'] = True
            self.fields['short_url'].widget.attrs['readonly'] = True

    
    def clean_url(self):
        value = self.cleaned_data.get('url')
        if self.instance.pk and value != self.instance.url:
            raise forms.ValidationError("原始網址無法修改。")
        return value
    
    def clean_short_url(self):
        value = self.cleaned_data.get('short_url')
        if self.instance.pk:
            if value != self.instance.short_url:
                raise forms.ValidationError("短網址代碼無法修改")
            return value
        if value:
            if len(value) > 8:
                raise forms.ValidationError("短網址代碼不能超過8個字元")
            elif not re.fullmatch(r'[A-Za-z0-9]+', value):
                raise forms.ValidationError("短網址代碼只能包含英數字")
            elif ShortURL.objects.filter(short_url=value).exists():
                raise forms.ValidationError("此短網址已被使用")
        return value

    def clean(self):
        cleaned_data = super().clean()
        if not self.instance.pk and not cleaned_data.get('short_url'):
            while True:
                code = generate_code()
                if not ShortURL.objects.filter(short_url=code).exists():
                    cleaned_data['short_url'] = code
                    break
        return cleaned_data
