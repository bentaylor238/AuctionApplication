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
    username = forms.CharField(label='User Name', max_length=50)
    email = forms.CharField(label="Email", max_length=100)
    password = forms.CharField(label='Password', max_length=100)
    confirm_password = forms.CharField(label='Confirm Password', max_length=100)

class BidForm(forms.Form):
    amount = forms.FloatField(label='Amount in $:')