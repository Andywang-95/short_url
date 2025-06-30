from django.http import HttpResponse
from django.urls import reverse
from django.shortcuts import redirect

def htmx_redirect(request, url, **kwargs):
    if request.headers.get("HX-Request") == "true":
        response = HttpResponse("", status=200)
        response["HX-Redirect"] = reverse(url, kwargs=kwargs)
        return response
    return redirect(url, kwargs=kwargs)