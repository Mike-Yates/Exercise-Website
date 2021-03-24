from django import forms


class InfoForm(forms.Form):
    # need to implement this
    your_name = forms.CharField(label='your name')
