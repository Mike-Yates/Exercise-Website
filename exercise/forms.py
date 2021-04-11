from django.forms import ModelForm
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django import forms

from exercise.models import Exercise, Bmi



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


class ExerciseForm(ModelForm):
    '''
    Form for storing user exercises
    '''
    class Meta:
        model = Exercise
        fields = ('exercise_name', 'reps', 'sets', 'weight_in_pounds')


# You can create other forms here to use (for example the one to be used on first login, but you have to still create a new page to then use the form in)


class BmiForm(ModelForm):
    '''
    Form for storing user height/weight, to calculate the user's bmi
    '''
    class Meta:
        model = Bmi
        fields = ('height_feet', 'height_inches', 'weight_pounds')
        # not included: user_bmi, timestamp
