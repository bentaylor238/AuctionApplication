from django import forms
from django.contrib.auth.forms import UserCreationForm, UserChangeForm, PasswordChangeForm
from .models import Rule, AuctionUser, Auction, SilentItem, LiveItem
class RulesForm(forms.ModelForm):
    class Meta:
        model = Rule
        fields = ('title', 'rules_content', 'announcements_content')

class BidForm(forms.Form):
    amount = forms.FloatField(label='Amount in $:')

class CreateAccountForm(UserCreationForm):
    class Meta:
        model = AuctionUser
        fields = ('first_name','last_name', 'username','email',)

class CreateAccountFormHiddenPass(UserCreationForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['password1'].widget = forms.HiddenInput()
        self.fields['password2'].widget = forms.HiddenInput()
    class Meta:
        model = AuctionUser
        fields = ('first_name','last_name','username','email',)

class UpdateAccountForm(UserChangeForm):
    class Meta:
        model = AuctionUser
        fields = ('first_name','last_name', 'username','email','auction_number')

class AuctionForm(forms.ModelForm):
    class Meta:
        model = Auction
        fields = ('published', 'type')
    
class SilentItemForm(forms.ModelForm):
    class Meta:
        model = SilentItem
        fields = ('title','description','image','auction')
        widgets = { 
            'end': forms.DateTimeInput(
                attrs={'type':'datetime-local'}, 
                format='%Y-%m-%dT%H:%M' #this is to match the html datetime-local format
            ),
            'auction':forms.HiddenInput()
        }

class LiveItemForm(forms.ModelForm):
    class Meta:
        model = LiveItem
        fields = ('title','description','image','auction')
        widgets = {
            'auction':forms.HiddenInput()
        }

class ChangePasswordForm(forms.Form):
    password1 = forms.CharField(widget=forms.PasswordInput())
    password2 = forms.CharField(widget=forms.PasswordInput())
    user = forms.ModelChoiceField(queryset=AuctionUser.objects.all(), empty_label="Select A User")

    def clean(self):
        cleaned_data = super().clean()
        password1 = self.cleaned_data.get('password1')
        password2 = self.cleaned_data.get('password2')
        if password1 and password2:
            if password1 != password2:
                raise forms.ValidationError("Passwords do not match")
            return cleaned_data

#SAVED FOR AN EXAMPLE, NOT USED
# class CreateAccount(forms.Form):
#     first_name = forms.CharField(label='First Name', max_length=50)
#     last_name = forms.CharField(label='Last Name', max_length=50)
#     new_username = forms.CharField(label='User Name', max_length=50)
#     email = forms.EmailField(label="Email", max_length=100)
#     new_password = forms.CharField(widget=forms.PasswordInput())
#     confirm_password = forms.CharField(widget=forms.PasswordInput())
#     def clean(self):
#         cleaned_data = super().clean()
#         password = self.cleaned_data.get('new_password') #get value from new_password
#         confirm_password = self.cleaned_data.get('confirm_password') #get value from confirm_password
        
#         if password and confirm_password:
#             if password != confirm_password:
#                 raise forms.ValidationError('Passwords do not match')
#             return password
