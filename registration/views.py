
from django.shortcuts import render,redirect
from .forms import UserCreationForm ## this is the overridden form with email field included
## from django.contrib.auth.forms import UserCreationForm ## we don't need this anymore
from django.contrib.auth.models import User



def index(request):
    return render(request, 'registration/index.html', {"some_data": "cenk arda"})

def mainpage(request):
    usercount = User.objects.count()
    return render(request,'registration/mainpage.html',{'usercount': usercount })




def home(request):
    return render(request,'registration/home.html')
# Create your views here.
def signup(request):
    if request.method =='POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('login')
    else:
        form = UserCreationForm()
    return render(request,'registration/signup.html',{'form':form})

"""def login_user(request):
    if request.method == 'POST':
        # create a form instance and populate it with data from the request:
        form = LoginForm(request.POST)

        if form.is_valid():
            data = form.cleaned_data
            user = authenticate(username=data['username'],password=data['password'])
            if user is None:
              render(request,'registration/login.html', {'ctx': True})
            else:
                redirect('mainpage')
            # process the data in form.cleaned_data as required
            # ...
            # redirect to a new URL:


            return redirect('')

            # if a GET (or any other method) we'll create a blank form
    else:

        form = LoginForm()
    return render(request, 'registration/login.html', {'form': form})"""

"""def login_error(request):
    return render(request, 'registration/login.html', {'ctx': True})"""