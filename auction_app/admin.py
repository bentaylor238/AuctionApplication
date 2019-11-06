from django.contrib import admin
from .models import *

from django.contrib.auth import get_user_model
from django.contrib.auth.admin import UserAdmin
from django.contrib.auth.models import User
from .forms import CreateAccountForm, UpdateAccountForm

from .models import AuctionUser, Rule

class AuctionUserAdmin(UserAdmin):
    add_form = CreateAccountForm
    form = UpdateAccountForm
    model = AuctionUser
    # list_display = ['first_name','last_name','email',]

admin.site.register(AuctionUser, AuctionUserAdmin)
admin.site.register(Rule)
admin.site.register(SilentItem)
admin.site.register(BidLive)
admin.site.register(LiveItem)
admin.site.register(BidSilent)
admin.site.register(User)
admin.site.register(Auction)
