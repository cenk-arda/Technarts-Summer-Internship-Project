from django import forms
from django.contrib.auth.forms import UserChangeForm
from django.contrib.auth.models import User
from .models import Comment
from registration.models import MyUser


class EditProfileForm(UserChangeForm):
    class Meta:
        model = User
        fields = ['email', 'first_name', 'last_name']
        widgets = {
            'email': forms.EmailInput(attrs={'required': 'true'}),
            'first_name': forms.TextInput(attrs={'required': 'true'}),
            'last_name': forms.TextInput(attrs={'required': 'true'}),
        }


class AddReviewForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ['text','rate']
        widgets = {
            'text': forms.Textarea(attrs={'rows': 3, 'cols': 100,
                                          'placeholder': 'What do you think about this meal? (Note: max 250 chars)'})
        }
        labels = {
            'text': "It's review time!",
            'rate': "Evaluate this meal over 5 stars."
        }

class AddImageForm(forms.ModelForm):
    class Meta:
        model = MyUser
        fields = '__all__'
        exclude = ['user','about']

class ChangeAboutForm(forms.ModelForm):
    class Meta:
        model = MyUser
        fields = ['about']