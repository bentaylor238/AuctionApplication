from django.shortcuts import render
# from .models


def index(request):
    context={}
    return render(request, 'auction_app/index.html', context)
