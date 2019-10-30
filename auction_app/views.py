from django.shortcuts import render
from auction_app.models import Rules, User
from django.utils import timezone
from .forms import *
from django.http import HttpResponse, JsonResponse, HttpResponseRedirect
from django.shortcuts import redirect
from django.contrib.auth.forms import UserCreationForm
from django.urls import reverse_lazy
from django.views import generic
#from django.contrib.auth.models import User
#from django.contrib.auth import authenticate



def home(request):
    context={'admin':False}#data to send to the html page goes here
    return render(request, 'home.html', context)

def live(request):
    context={}#data to send to the html page goes here
    return render(request, 'live.html', context)

def login(request):
    context={}#data to send to the html page goes here
    return render(request, 'login.html', context)

def payment(request):
    context={}#data to send to the html page goes here
    return render(request, 'payment.html', context)

def rules(request):
    if Rules.objects.count() == 0:
        setDefaultRules()
    context = {
        "admin":True,
        "rules": Rules.objects.all().get(pk=1),
        "form":RulesForm()}
    return render(request, 'rules.html', context)

def setDefaultRules():
    f = open('auction_app/static/txt/defaultRules.txt', 'r')
    defaultRules = f.read()
    f.close()
    f = open('auction_app/static/txt/defaultAnnouncements.txt', 'r')
    defaultAnnouncements = f.read()
    f.close()
    rules = Rules(title="Rules & Announcements",
                  lastModified=timezone.now(),
                  rulesContent=defaultRules,
                  announcementsContent=defaultAnnouncements
                  )
    rules.save()

def silent(request):
    context={}#data to send to the html page goes here
    return render(request, 'silent.html', context)

def users(request):
    context={}#data to send to the html page goes here
    return render(request, 'users.html', context)

def login(request, login_form=Login(), create_account_form=CreateAccount()):
    if request.method == 'POST':
        for key in request.GET:
            print(f"\t{key} => {request.GET[key]}")
        login_form = Login(request.POST)
        if login_form.is_valid():
            return redirect(rules)
        else:
            context={
                #data to send to the html page goes here
                'login_form': login_form, #defaults to a blank Login() object
                'create_account_form': create_account_form, #defaults to a blank CreateAccount() object
                'loginPage': True
            }
            return render(request, 'login.html', context)
    username = None
    password = None
    return render(request, 'login.html', context)

    # if 'username' in request.GET:
    #     username = request.GET['username']
    # else:
    #     return render(request, 'login.html', context)
    # if 'password' in request.GET:
    #     password = request.GET['password']
    # else:
    #     return render(request, 'login.html', context)

    # try:
    #     user = User.objects.get(username=username)
    # except:
    #     return render(request, 'login.html', context)
    #     #return JsonResponse({'error': 'The given username is not in our database :('})

    # if user.password == password:
    #     return redirect(rules)
    # else:
    #     return render(request, 'login.html', context)
    #     #return JsonResponse({'error': 'The given password does not match the username :('})

    """
        user = authenticate(username=username, password=password)
        if user is not None:
            # User is authenticated
        else:
            # No user exists
    """

def create_account(request):

    if request.method == 'POST':
        for key in request.POST:
            print(f"\t{key} => {request.POST[key]}")
        create_account_form = CreateAccount(request.POST)
        if create_account_form.is_valid():
            #create user model and save
            username = request.POST['new_username']
            email = request.POST['email']
            password = request.POST['new_password']
            firstname = request.POST['first_name']
            lastname = request.POST['last_name']
            new_user = User(name=firstname+" "+lastname, username=username, email=email, password=password)
            new_user.save()
            print("user created: " + username)
            return redirect(rules)
        else:
            #call the login view passing in the form to render
            return login(request, create_account_form=create_account_form)
            
        '''try:
            user = User.objects.create_user(username, email=username,password=password1)
            user.save()
        except:
            print("Something went wrong in creating the user")
            # no idea at the moment how to handle
    #not sure how to handle any of the else statements yet'''

class SignUp(generic.CreateView):
    form_class = UserCreationForm
    success_url = reverse_lazy('rules')
    template_name = 'signup.html'