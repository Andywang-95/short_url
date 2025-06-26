from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.views.decorators.http import require_POST
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from .forms import CustomUserCreationForm as UserCreationForm
from common.decorators import htmx_required

@htmx_required
def sign_in(request):
    return render(request, 'users/sign_in.html')

@htmx_required
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

@require_POST
def create_session(request):
    email = request.POST.get('email')
    password = request.POST.get('password')or request.POST.get('password2')
    if email and password:
        user = authenticate(request, username=email, password=password)
        if user is not None:
            login(request, user)
            return redirect('shorturls:index')
        else:
            messages.error(request, 'Email 或 密碼 錯誤，請重新確認')
    else:
        messages.error(request, '請輸入 Email 和 密碼')

@login_required
@require_POST
def delete_session(request):
    user = request.user
    if user.is_authenticated:
        logout(request)
        messages.success(request, '成功登出')
        return redirect('home')