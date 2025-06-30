from bs4 import BeautifulSoup
import requests
from django.db.models.functions import Coalesce
from shorturls.models import ShortURL
from django.http import HttpResponse
from django.urls import reverse
from urllib.parse import urlparse, parse_qs

def all_shorturls(user):
    shorturls = (
            user.shorturls
            .annotate(
                latest_time=Coalesce('updated_at', 'created_at')
            )
            .prefetch_related('utm')
            .order_by('-latest_time')
        )
    return shorturls


def detail_shorturl(user, code):
    shorturl = ShortURL.objects.select_related('utm').get(created_by=user, short_url=code)
    return shorturl

def url_utm_params(url):
    parsed_url = urlparse(url)
    query_params = parse_qs(parsed_url.query)
    utm_data = {
        'source': query_params.get('utm_source', [None])[0],
        'medium': query_params.get('utm_medium', [None])[0],
        'campaign': query_params.get('utm_campaign', [None])[0],
        'term': query_params.get('utm_term', [None])[0],
        'content': query_params.get('utm_content', [None])[0],
    }
    utm_data = {k: v for k, v in utm_data.items() if v is not None}
    return utm_data

def get_descriptions(request, url):
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/114.0.0.0 Safari/537.36',
        'Accept-Language': 'zh-TW,zh;q=0.9,en-US;q=0.8,en;q=0.7',
        'Referer': url,
    }
    try:
        resp = requests.get(url, headers=headers, timeout=5)
        resp.raise_for_status()
        resp.encoding = resp.apparent_encoding
        soup = BeautifulSoup(resp.text, 'html.parser')
        desc_tag = soup.find('meta', attrs={'name': 'description'})
        if desc_tag and desc_tag.get('content'):
            return desc_tag['content']
        else:
            return None
    except requests.RequestException as e:
        print(f"取得描述失敗: {e}")
    return None