from django.shortcuts import render
from auction_app.models import Rules, AuctionUser
from django.utils import timezone
from .forms import *
from django.http import HttpResponse, JsonResponse, HttpResponseRedirect
from django.shortcuts import redirect
from django.contrib.auth.forms import UserCreationForm
from django.urls import reverse_lazy
from django.views import generic
# from django.contrib.auth.models import User
#from django.contrib.auth import authenticate



def home(request):
    context={}#data to send to the html page goes here
    return render(request, 'home.html', context)

def live(request):
    context={}#data to send to the html page goes here
    return render(request, 'live.html', context)

def payment(request):
    users = AuctionUser.objects.all()
    context={"users": users}#data to send to the html page goes here
    return render(request, 'payment.html', context)

def rules(request):
    if Rules.objects.count() == 0:
        rules = getDefaultRules()
        rules.save()
    else:
        rules = Rules.objects.get()

    if request.method == "POST":
        form = RulesForm(request.POST, instance=rules) # this way, we save a rules object to the db via a RulesForm
        form.save()
        return redirect(home)
    else:
        form = RulesForm(instance=rules)
        context = {
            "rules": rules,
            "form":form}
        return render(request, 'rules.html', context)

def getDefaultRules():
    f = open('auction_app/static/txt/defaultRules.txt', 'r')
    defaultRules = f.read()
    f.close()
    f = open('auction_app/static/txt/defaultAnnouncements.txt', 'r')
    defaultAnnouncements = f.read()
    f.close()
    return Rules(title="Rules & Announcements",
                last_modified=timezone.now(),
                rules_content=defaultRules,
                announcements_content=defaultAnnouncements)
                    
def silent(request):
    context={}#data to send to the html page goes here
    return render(request, 'silent.html', context)

def users(request):
    users = AuctionUser.objects.all()
    form = CreateAccountForm()
    if request.method == 'POST':
        form = CreateAccountForm(request.POST)
        #This part is what's broken, fix this to get password auto put into form
        # form.cleaned_data['password1'] = "ax7!bwaBc"
        # form.cleaned_data['password2'] = "ax7!bwaBc"
        if form.is_valid(): #passing passwords hiddenly so this should work
            #save data
            print("test\n")
            form.save()
        else:
            context = {
                "users": users,
                "form":form}
            return render(request, 'users.html', context)
    else:
        #first visit
        context={"users": users,
                 "form": form}#data to send to the html page goes here
        return render(request, 'users.html', context)

def afterLogin(request):
    if request.user.is_superuser:
        return redirect(home)
    else:
        return redirect(rules)


def updateAuctionNumber(request):
    #do update
    for key in request.POST:
        print(f"\t{key} => {request.POST[key]}")
    username = request.POST['username']
    user = AuctionUser.objects.get(username=username)
    user.auction_number = request.POST['auction_number']
    user.save()
    return redirect(users)

#LEFT HERE FOR EXAMPLES, AREN'T BEING USED
# def login(request, login_form=Login(), create_account_form=CreateAccount()):
#     if request.method == 'POST':
#         for key in request.GET:
#             print(f"\t{key} => {request.GET[key]}")
#         login_form = Login(request.POST)
#         if login_form.is_valid():
#             return redirect(rules)
#         else:
#             context={
#                 #data to send to the html page goes here
#                 'login_form': login_form, #defaults to a blank Login() object
#                 'create_account_form': create_account_form, #defaults to a blank CreateAccount() object
#                 'loginPage': True
#             }
#             return render(request, 'login.html', context)
#     username = None
#     password = None
#     return render(request, 'login.html', context)


# def create_account(request):

#     if request.method == 'POST':
#         for key in request.POST:
#             print(f"\t{key} => {request.POST[key]}")
#         create_account_form = CreateAccount(request.POST)
#         if create_account_form.is_valid():
#             #create user model and save
#             username = request.POST['new_username']
#             email = request.POST['email']
#             password = request.POST['new_password']
#             firstname = request.POST['first_name']
#             lastname = request.POST['last_name']
#             new_user = User(name=firstname+" "+lastname, username=username, email=email, password=password)
#             new_user.save()
#             print("user created: " + username)
#             return redirect(rules)
#         else:
#             #call the login view passing in the form to render
#             return login(request, create_account_form=create_account_form)

     
class CreateAccount(generic.CreateView):
    form_class = CreateAccountForm
    success_url = reverse_lazy('afterLogin')
    template_name = 'createAccount.html'

    # def form_valid(self, form):
    #     #This method is called when valid form data has been POSTed.
    #     #It should return an HttpRespons
    #     if form.password:
    #         return super().form_valid(form)
    #     else:
    #         return #something
