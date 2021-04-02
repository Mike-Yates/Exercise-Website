from django import forms
from django.contrib.auth.models import User
from .models import *


# The form for initial info. This uses a ModelForm based on the fields we tell it. This is the easiest way to
# directly modify a profile with a form
class InfoForm(forms.ModelForm):
    class Meta:
        model = Profile
        # need to change these to the fields we want to display.
        fields = ('bio', 'location', 'birth_date', 'height', 'weight')
        # fields = ('bio', 'location')
