from django.contrib import admin
from django.contrib.auth import get_user_model
from django.contrib.auth.admin import UserAdmin
from django.contrib.auth.models import User
from .forms import CreateAccount, UpdateAccount

from .models import AuctionUser, Rules

class AuctionUserAdmin(UserAdmin):
    add_form = CreateAccount
    form = UpdateAccount
    model = AuctionUser
    # list_display = ['first_name','last_name','email',]

admin.site.register(AuctionUser, AuctionUserAdmin)
admin.site.register(Rules)
