from django.urls import path, include
from django.contrib import admin
from . import views

urlpatterns = [
    path('index', views.home, name='home'),
    path('home', views.home, name='home'),
    path('live', views.live, name='live'),
    path('silent', views.silent, name='silent'),
    path('users', views.users, name='users'),
    path('payment', views.payment, name='payment'),
    # path('login', views.login, name='login'),
    path('create_account', views.create_account, name='create_account'),
    path('rules', views.rules, name='rules'),
    path('admin/', admin.site.urls),
    path('signup/', views.SignUp.as_view(), name='signup'),
    path('', include('django.contrib.auth.urls')),
]