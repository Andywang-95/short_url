from django.http import HttpResponse
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.views.decorators.http import require_POST
from django.contrib import messages
from common.decorators import htmx_required
from .forms import ShortURLForm
from .models import UTM, ShortURL
from .services import all_shorturls, detail_shorturl, url_utm_params, get_descriptions
from common.utils import htmx_redirect
from django.conf import settings
short_url_base = settings.SHORT_URL_BASE


def home(request):
    if request.user.is_authenticated:
        return index(request)
    return render(request, 'base.html')

@login_required
def index(request):
    user = request.user
    if user.is_authenticated:
        urls = all_shorturls(user)
    return render(request, 'base.html', {
        'urls': urls, 'short_url_base': short_url_base})

@login_required
@htmx_required
def new(request):
    form = ShortURLForm()
    return render(request, 'shorturls/new.html',{'form': form, 'short_url_base': short_url_base})

@login_required
@require_POST
@htmx_required
def create(request):
    form = ShortURLForm(request.POST)
    if form.is_valid():
        short_url = form.save(commit=False)
        short_url.created_by = request.user
        short_url.save()
        
        utm_data = url_utm_params(short_url.url)
        try:
            if utm_data:
                print('開始建立UTM資訊')
                UTM.objects.create(short_url=short_url, **utm_data)
            messages.success(request, '短網址建立成功！')
            urls = all_shorturls(request.user)
        except Exception as e:
            messages.warning(request, '短網址建立成功，但UTM資訊不完整，可能無法準確追蹤。')
        return render(request, 'shorturls/index.html', {'urls': urls, 'short_url_base': short_url_base})
    else:
        messages.error(request, '短網址建立失敗，請檢查輸入的資料。')
        return render(request, 'shorturls/new.html', {'form': form, 'short_url_base': short_url_base})

@login_required
@htmx_required
def detail(request, code):
    user = request.user
    try:
        url = detail_shorturl(user, code)
        print(url)
        return render(request, 'shorturls/detail.html', {'url': url, 'short_url_base': short_url_base})
    except Exception as e:
        print(f"Exception occurred: {e}")
        messages.error(request, '找不到該短網址或您沒有權限查看。')
        return htmx_redirect(request, 'shorturls:index')

@login_required
@htmx_required
@require_POST
def delete(request, code):
    user = request.user
    try:
        url = detail_shorturl(user, code)
        url.delete()
        messages.success(request, '短網址已成功刪除。')
    except Exception as e:
        messages.error(request, f'刪除短網址失敗: {e}')
    return htmx_redirect(request, 'shorturls:index')

@login_required
@htmx_required
def edit(request, code):
    user = request.user
    shorturl = detail_shorturl(user, code)
    form = ShortURLForm(instance=shorturl)
    return render(request, 'shorturls/edit.html', {'form': form, 'url': shorturl, 'short_url_base': short_url_base})


@login_required
@htmx_required
@require_POST
def update(request, code):
    user = request.user
    shorturl = detail_shorturl(user, code)
    form = ShortURLForm(request.POST, instance=shorturl)
    if form.is_valid():
        form.save()
        messages.success(request, '短網址已成功更新。')
        urls = all_shorturls(request.user)
        return render(request, 'shorturls/index.html', {'urls': urls, 'short_url_base': short_url_base})
    messages.error(request, '更新短網址失敗，請檢查輸入的資料。')
    return render(request, 'shorturls/edit.html', {'form': form, 'url': shorturl, 'short_url_base': short_url_base})

def copy_shortUrl(request):
    messages.success(request, '短網址已複製到剪貼簿。')
    print("複製短網址成功")
    return render(request, 'partial/messages.html')

def get_context(request):
    url = request.GET.get("url")
    print(f"取得頁面資訊的URL: {url}")
    context = get_descriptions(request, url)
    if context:
        return HttpResponse(context)
    messages.error(request, '無法取得頁面資訊')
    return render(request, 'partial/messages.html')


@login_required
@htmx_required
@require_POST
def toggle_active(request, code):
    is_active = request.POST.get("is_active") == "on"
    shorturl = detail_shorturl(request.user, code)
    shorturl.is_active = is_active
    shorturl.save()
    if is_active:
        messages.success(request, f'短網址已啟用。')
    else:
        messages.warning(request, f'短網址已停用。')
    return render(request, 'partial/messages.html')


def redirect_view(request, code):
    shorturl = get_object_or_404(ShortURL, short_url=code, is_active=True)

    # 無密碼：直接跳轉
    if not shorturl.password:
        return render(request, "shorturls/redirect_page.html", {"target_url": shorturl.url})

    # 有密碼：處理驗證
    if request.method == "POST":
        input_password = request.POST.get("password")
        if input_password == shorturl.password:
            return render(request, "shorturls/redirect_page.html", {"target_url": shorturl.url})
        else:
            messages.error(request, "密碼錯誤，請再試一次")

    return render(request, "shorturls/password_page.html", {"code": code})