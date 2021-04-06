from django.contrib.auth.forms import UserCreationForm
from django.shortcuts import render
from django.views import generic
from django.http import HttpResponseRedirect
from django.urls import reverse
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from .forms import CreateUserForm


@login_required(login_url='login')
def home(request):
    context = {}
    return render(request, 'exercise/home.html', context)


def login_user(request):
    if request.user.is_authenticated:
        return HttpResponseRedirect(reverse('exercise:home'))
    else:
        if request.method == 'POST':
            username = request.POST.get('username')
            password = request.POST.get('password')
            user = authenticate(request, username=username, password=password)

            if user is not None:
                login(request, user)
                return HttpResponseRedirect(reverse('exercise:home'))
            else:
                messages.info(
                    request, 'Username OR Password is Incorrect, Please try again')

        context = {}
        return render(request, 'exercise/login.html', context)


def logout_user(request):
    logout(request)
    return render(request, 'exercise/index.html')


def register_page(request):
    if request.user.is_authenticated:
        return HttpResponseRedirect(reverse('exercise:home'))
    else:
        form = CreateUserForm()

        if request.method == 'POST':
            form = CreateUserForm(request.POST)

            if form.is_valid():
                form.save()
                user = form.cleaned_data.get('username')
                messages.success(request, "User Created for " + user)
                return HttpResponseRedirect(reverse('exercise:login'))

    context = {'form': form}
    return render(request, 'exercise/register.html', context)
