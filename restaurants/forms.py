from django import forms
from django.contrib.auth.forms import UserChangeForm
from django.contrib.auth.models import User
from .models import Comment

class EditProfileForm(UserChangeForm):

    class Meta:
        model = User
        fields =  ['email','first_name', 'last_name']
        widgets = {
            'email': forms.EmailInput(attrs={'required': 'true'}),
            'first_name': forms.TextInput(attrs={'required': 'true'}),
            'last_name': forms.TextInput(attrs={'required': 'true'}),
        }


class AddReviewForm(forms.ModelForm):

    class Meta:
        model = Comment
        fields = ['text']
        widgets = {
            'text': forms.Textarea(attrs={'rows':3, 'cols':15, 'placeholder': 'What do you think about this meal? (Note: max 250 chars)'})
        }
        labels = {
            'text': "It's review time!"
        }