from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User


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

    def save(self, commit=True):
        user = super(UserCreationForm, self).save(commit=False)  ## create a modelform but don't send it to the database yet.
        user.email = self.cleaned_data['email']
        user.first_name = self.cleaned_data['first_name']
        user.last_name = self.cleaned_data['last_name']

        if commit:  ##when customization/changes ends, commit gets its default value (True)
            user.save()

        return user
