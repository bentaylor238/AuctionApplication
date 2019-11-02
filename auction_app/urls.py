from django.urls import path, include
from django.contrib import admin
from . import views

urlpatterns = [
<<<<<<< HEAD
    path('init_test_db', views.init_test_db, name="init_test_db"),
=======
    path('submit_bid', views.submit_bid, name='submit_bid'),
>>>>>>> 44606aba3957b193abe946d99db777adb0fe5db7
    path('index', views.home, name='home'),
    path('home', views.home, name='home'),
    path('live', views.live, name='live'),
    path('silent', views.silent, name='silent'),
    path('users', views.users, name='users'),
    path('payment', views.payment, name='payment'),
    path('afterLogin',views.afterLogin, name='afterLogin'),
    # path('login', views.login, name='login'),
    # path('create_account', views.create_account, name='create_account'),
    path('rules', views.rules, name='rules'),
    path('create_account', views.CreateAccount.as_view(), name='create_account'),
    path('', include('django.contrib.auth.urls')), #auth.urls includes the login url
    path('',views.home, name='home'),
    path('updateAuctionNumber', views.updateAuctionNumber, name='updateAuctionNumber')
]