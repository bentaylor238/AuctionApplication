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
    fieldsets = UserAdmin.fieldsets + (
        (None, {
            'fields':
            ('auction_number','has_paid','amount')
        }),
    )

class BidAdmin(admin.ModelAdmin):
    list_display = ('user', 'item', 'amount')


admin.site.site_header = "Auction Admin"

admin.site.register(AuctionUser, AuctionUserAdmin)
admin.site.register(Rule)
admin.site.register(SilentItem)
admin.site.register(LiveItem)
admin.site.register(BidSilent, BidAdmin)
admin.site.register(User)
admin.site.register(Auction)

