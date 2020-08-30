from django.shortcuts import render, redirect
from .forms import UserCreationForm  ## this is the overridden form with email field included
## from django.contrib.auth.forms import UserCreationForm ## we don't need this anymore
from django.contrib.auth.models import User
from django.views import View



class Home(View):
    def get(self, request, *args, **kwargs):
        return render(request, 'registration/home.html')


class Signup(View):
    template_name = 'registration/signup.html'

    def get(self, request, *args, **kwargs):
        form = UserCreationForm()
        return render(request, self.template_name, {'form': form})

    def post(self, request, *args, **kwargs):
        form = UserCreationForm(request.POST)
        if form.is_valid() and form.mail_is_unique():
            form.save()
            return redirect('login')
        return render(request, self.template_name, {'form': form})


"""def signup(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid() and form.mail_is_unique():
            form.save()
            return redirect('login')
    else:
        form = UserCreationForm()
    return render(request, 'registration/signup.html', {'form': form})"""
