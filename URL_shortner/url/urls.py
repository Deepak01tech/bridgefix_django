from django.urls import path
from . import views

app_name = 'url'
urlpatterns = [
    path('', views.shorten_url, name='shorten_url'),
    path('<slug:slug>/', views.url_redirect, name='url_redirect'),
]