from django import forms
from .models import Rules
# from crispy_forms.helper import FormHelper

class RulesForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super(RulesForm, self).__init__(*args, **kwargs)
        # self.helper = FormHelper()
    class Meta:
        model = Rules
        fields = ('title', 'rulesContent', 'announcementsContent')

class CreateAccount(forms.Form):
    first_name = forms.CharField(label='First Name', max_length=50)
    last_name = forms.CharField(label='Last Name', max_length=50)
    new_username = forms.CharField(label='User Name', max_length=50)
    email = forms.EmailField(label="Email", max_length=100)
    new_password = forms.CharField(widget=forms.PasswordInput())
    confirm_password = forms.CharField(widget=forms.PasswordInput())
    def clean(self):
        cleaned_data = super().clean()
        password = self.cleaned_data.get('new_password') #get value from new_password
        confirm_password = self.cleaned_data.get('confirm_password') #get value from confirm_password
        
        if password and confirm_password:
            if password != confirm_password:
                raise forms.ValidationError('Passwords do not match')
            return password

class Login(forms.Form):
    username = forms.CharField(label='User Name', max_length=50)
    password = forms.CharField(widget=forms.PasswordInput())

class BidForm(forms.Form):
    amount = forms.FloatField(label='bid', required=False)

    def clean_amount(self):
        data = self.cleaned_data['amount']
        if data < 0:
            raise forms.ValidationError("Cannot enter in negative values")

        # Always return a value to use as the new cleaned data, even if
        # this method didn't change it.
        return data
    
    email = forms.CharField(label="Email", max_length=100)
    password = forms.CharField(label='Password', max_length=100)
    confirm_password = forms.CharField(label='Confirm Password', max_length=100)

class BidForm(forms.Form):
    amount = forms.FloatField(label='Amount in $:')
