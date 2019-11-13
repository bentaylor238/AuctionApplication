from django.urls import path, include
from django.contrib import admin
from . import views

urlpatterns = [
    path('delete_item', views.delete_item, name="delete_item"),
    path('create_item', views.create_item, name="create_item"),
    path('sellLiveItem', views.sellLiveItem, name='sellLiveItem'),
    path('updateAuctionNumber', views.updateAuctionNumber, name='updateAuctionNumber'),
    path('init_test_db', views.init_test_db, name="init_test_db"),
    path('submit_bid', views.submit_bid, name='submit_bid'),
    path('index', views.home, name='home'),
    path('home', views.home, name='home'),
    path('live', views.live, name='live'),
    path('silent', views.silent, name='silent'),
    path('users', views.users, name='users'),
    path('payment', views.payment, name='payment'),
    path('updateUserPayment', views.updateUserPayment, name='updateUserPayment'),
    path('afterLogin',views.afterLogin, name='afterLogin'),
    path('rules', views.rules, name='rules'),
    path('create_account', views.create_account, name='create_account'),
    path('', include('django.contrib.auth.urls')), # auth.urls includes the login url
    path('', views.home, name='home'),
    path('updateAuctionNumber', views.updateAuctionNumber, name='updateAuctionNumber')
]