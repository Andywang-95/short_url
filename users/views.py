from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.views.decorators.http import require_POST
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from .forms import CustomUserCreationForm as UserCreationForm
from shorturls import views as shorturls_views


def sign_up(request):
    form = UserCreationForm()
    return render(request, 'users/sign_up.html', {'form': form})

@require_POST
def create(request):
    form = UserCreationForm(request.POST)
    if form.is_valid():
        user = form.save()
        return create_session(request)
    else:
        messages.error(request, '註冊失敗，請檢查輸入的資料是否正確')
    return render(request, 'users/sign_up.html', {'form': form})

