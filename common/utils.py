from django.http import HttpResponse
from django.urls import reverse
from django.shortcuts import redirect

def htmx_redirect(request, url):
    if request.headers.get("HX-Request") == "true":
        response = HttpResponse()
        response["HX-Redirect"] = reverse(url)
        return response
    else:
        return redirect(url)