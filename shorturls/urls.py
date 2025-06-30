from django.urls import path
from . import views

app_name = 'shorturls'

urlpatterns = [
    path('', views.home, name='home'),
    path('', views.index, name='index'),
    path('new/', views.new, name='new'),
    path('create/', views.create, name='create'),
    path('<str:code>/', views.detail, name='detail'),
    path('<str:code>/delete', views.delete, name='delete'),
    path('<str:code>/edit', views.edit, name='edit'),
    path('<str:code>/update', views.update, name='update'),
    # path('<str:short_code>/', views.redirect_to_long_url, name='redirect_to_long_url'),
    # path('stats/<str:short_code>/', views.url_stats, name='url_stats'),
]
