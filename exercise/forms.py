from django.forms import ModelForm
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django import forms


class CreateUserForm(UserCreationForm):
    '''
    Form to be used when registering a new user manually without the use
    of google authentication.

    Uses the built in user model from Django (We don't need to create a new user Profile)
    '''
    class Meta:
        model = User
        # Information to be collected when registering a new user.
        fields = ['username', 'email', 'password1', 'password2']


# You can create other forms here to use (for example the one to be used on first login, but you have to still create a new page to then use the form in)
