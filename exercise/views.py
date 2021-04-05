from django.contrib.auth.models import User, Group
from django.shortcuts import render
from django.views import generic
from .forms import *
from django.http import *


# view that makes users sign in or sends them to /home
def google_login(request):
    if request.user.is_authenticated:
        return HttpResponseRedirect('/home')
    else:
        return render(request, 'exercise/index.html')


# view that redirects first time users to a form and renders the homepage for already registered users
def home(request):
    if not request.user.is_authenticated:
        return HttpResponseRedirect('/')
    if not request.user.groups.filter(name='registered').exists():
        return HttpResponseRedirect('/infoform')
    else:
        return render(request, 'exercise/home.html')


# view that renders and saves a form for first time user info and then adds users to the registered group
def get_user_info(request):
    if request.method == 'POST':
        form = InfoForm(request.POST, instance=request.user.profile)
        if form.is_valid():
            my_group = Group.objects.get(name='registered')
            my_group.user_set.add(request.user)
            form.save()
            return HttpResponseRedirect('/home')
    else:
        form = InfoForm()
        return render(request, 'exercise/info_form.html', {'form': form})

class ProfileView(generic.CreateView):
    model = Profile
    fields = ['user', 'bio', 'location', 'birth_date']
    template_name = 'exercise/dash.html'
