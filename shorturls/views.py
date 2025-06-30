from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.views.decorators.http import require_POST
from django.contrib import messages
from django.db.models import Prefetch
from common.decorators import htmx_required
from .forms import ShortURLForm
from .models import UTM
from .services import all_shorturls, detail_shorturl, url_utm_params
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
        print(f"UTM Data: {utm_data}")  # Debugging line to check UTM data
        try:
            if utm_data:
                print('開始建立UTM資訊')
                UTM.objects.create(short_url=short_url, **utm_data)
            messages.success(request, '短網址建立成功！')
            urls = all_shorturls(request.user)
        except Exception as e:
            messages.warning(request, '短網址建立成功，但UTM資訊不完整，可能無法準確追蹤。')
        return render(request, 'shorturls/index.html', {'urls': urls})
    else:
        messages.error(request, '短網址建立失敗，請檢查輸入的資料。')
        return render(request, 'shorturls/new.html', {'form': form})

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
        return htmx_redirect(request, 'shorturls:detail', code=code)
    messages.error(request, '更新短網址失敗，請檢查輸入的資料。')
    return render(request, 'shorturls/edit.html', {'form': form, 'url': shorturl, 'short_url_base': short_url_base})

def copyShortUrl(request):
    messages.success(request, '短網址已複製到剪貼簿。')
    print("複製短網址成功")
    return render(request, 'partial/messages.html')