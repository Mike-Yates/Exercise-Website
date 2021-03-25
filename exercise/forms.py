from django import forms


# The form for initial info
class InfoForm(forms.Form):
    # need to implement this
    your_name = forms.CharField(label='your name')
