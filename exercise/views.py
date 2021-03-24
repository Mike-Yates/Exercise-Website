from django.shortcuts import render
from django.views import generic
from .forms import *
from django.http import *
from django.urls import *


def google_login(request):
    return render(request, 'exercise/index.html')


def home(request):
    return render(request, 'exercise/home.html')


def get_user_info(request):
    if request.method == 'POST':
        form = InfoForm(request.POST)
        if form.is_valid():
            # change the user data here
            return HttpResponseRedirect('/home')
    else:
        form = InfoForm()
        return render(request, 'exercise/info_form.html', {'form': form})
