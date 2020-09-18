from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from .models import MyUser


class LoginForm(forms.Form):
    username = forms.CharField(label='Username', max_length=200)
    password = forms.CharField(label='Password', max_length=32, widget=forms.PasswordInput)


class SignupForm(forms.Form):
    username = forms.CharField(label='Username', max_length=200)
    email = forms.EmailField(label='Email', max_length=200)
    password = forms.CharField(max_length=32, widget=forms.PasswordInput)


## by default, UserCreationForm does not have email field. i needed to override the class.
class UserCreationForm(UserCreationForm):
    email = forms.EmailField(required=True)

    class Meta:
        model = User
        fields = ['username', 'first_name', 'last_name', 'email', 'password1',
                  'password2']  ##by default, UserCreationForm has username,password1 and password2 fields.

    def mail_is_unique(self):
        username = self.cleaned_data['username']
        if User.objects.filter(email=self.cleaned_data['email']).exclude(username=username).count():
            return 0
        return 1

    def save(self, commit=True):
        user = super(UserCreationForm, self).save(
            commit=False)  ## create a modelform but don't send it to the database yet.
        user.email = self.cleaned_data['email']
        user.first_name = self.cleaned_data['first_name']
        user.last_name = self.cleaned_data['last_name']
        myuser = MyUser(user = user)

        if commit:  ##when customization/changes ends, commit gets its default value (True)
            user.save()
            myuser.save()

        return user




"""class SearchForm(forms.Form):
    input = forms.CharField()

    def get_results(self):
        input_data = self.cleaned_data['input']
        if input_data is not None:
            restaurants = Restaurant.objects.filter(Q(restaurant_name__icontains=query))
            meals = RestaurantsMeal.objects.filter(Q(meal_name__icontains=query))
            users = MyUser.objects.filter(Q(user__username__icontains=query) | Q(user__first_name__icontains=query) |
                                          Q(user__last_name__icontains=query) | Q(user__email__icontains=query))
            context = {'restaurants': restaurants, 'meals': meals, 'users': users}
            return context;"""
