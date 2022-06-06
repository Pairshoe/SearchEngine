from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('result/', views.search, name='result'),
    path('detail/', views.detail, name='detail'),
    path('about/', views.about, name='about'),
]
