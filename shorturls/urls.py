from django.urls import path
from . import views

app_name = 'shorturls'

urlpatterns = [
    path('', views.home, name='home'),
    path('', views.index, name='index'),
    path('new/', views.new, name='new'),
    path('create/', views.create, name='create'),
    path('<str:code>/detail', views.detail, name='detail'),
    path('<str:code>/delete', views.delete, name='delete'),
    path('<str:code>/edit', views.edit, name='edit'),
    path('<str:code>/update', views.update, name='update'),
    path('<str:code>/toggle_active', views.toggle_active, name='toggle_active'),
    path('copy_success', views.copy_shortUrl, name='copy_success'),
    path('get_description', views.get_context, name='get_context'),
    path('<str:code>/', views.redirect_view, name='redirect_view'),
]
