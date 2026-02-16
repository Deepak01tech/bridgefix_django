from django.urls import path
# from firstapp import views
from . import views

urlpatterns = [
    path('',views.member, name='members'),
    path('details/<int:id>/',views.details, name='details'),
]