
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
