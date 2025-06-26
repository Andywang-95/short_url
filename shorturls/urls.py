from django.urls import path
from . import views

app_name = 'shorturls'

urlpatterns = [
    path('', views.index, name='index'),
    path('create/', views.create, name='create'),
    # path('<str:short_code>/', views.redirect_to_long_url, name='redirect_to_long_url'),
    # path('stats/<str:short_code>/', views.url_stats, name='url_stats'),
]
