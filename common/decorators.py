from functools import wraps
from django.contrib import messages
from django.http import HttpResponseBadRequest

from django.shortcuts import redirect

def htmx_required(view_func):
    @wraps(view_func)
    def _wrapped_view(request, *args, **kwargs):
        if request.headers.get("HX-Request") == "true":
            return view_func(request, *args, **kwargs)
        messages.error(request, "請勿直接訪問此頁面")
        return redirect(request.META.get("HTTP_REFERER", "/"))
    return _wrapped_view
