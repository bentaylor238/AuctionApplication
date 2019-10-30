from django.contrib import admin
from django.contrib.auth import get_user_model
from django.contrib.auth.admin import UserAdmin
from .forms import CreateAccount, UpdateAccount

from .models import User

class UserAdmin(UserAdmin):
    add_form = CreateAccount
    form = UpdateAccount
    model = User
    list_display = ['email', 'username',]

admin.site.register(User, UserAdmin)
