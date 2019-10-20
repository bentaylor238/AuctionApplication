from django.urls import path

from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('index', views.index, name='index'),
    path('home', views.index, name='index'),
    path('live', views.live, name='live'),
    path('silent', views.silent, name='silent'),
    path('users', views.users, name='users'),
    path('payment', views.payment, name='payment'),
    path('login', views.login, name='login'),
    path('rules', views.rules, name='rules'),
]