from django import forms
from django.contrib.auth.forms import UserCreationForm, UserChangeForm
from .models import Rules, User

# from crispy_forms.helper import FormHelper

class RulesForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super(RulesForm, self).__init__(*args, **kwargs)
        # self.helper = FormHelper()
    class Meta:
        model = Rules
        fields = ('title', 'rulesContent', 'announcementsContent')

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

class Login(forms.Form):
    username = forms.CharField(label='User Name', max_length=50)
    password = forms.CharField(widget=forms.PasswordInput())

    def clean(self):
        cleaned_data = super().clean()
        username = self.cleaned_data.get('username')
        password = self.cleaned_data.get('password')

        if password and username:
            try:
                user = User.objects.get(username=username)
                if password != user.password:
                    #add validation error to the generic form
                    raise forms.ValidationError('Username or password is incorrect')
            except:
                #add validation error to specific form element
                self.add_error('username', 'Username does not exist')

class CreateAccount(UserCreationForm):
    class Meta:
        model = User
        fields = ('username', 'email')

class UpdateAccount(UserChangeForm):
    class Meta:
        model = User
        fields = ('username', 'email')