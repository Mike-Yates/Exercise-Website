from django.contrib.auth.forms import UserCreationForm
from django.shortcuts import render
from django.views import generic
from django.http import HttpResponseRedirect, JsonResponse, HttpResponse
from django.urls import reverse
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
import datetime
from .forms import CreateUserForm
from .models import Profile, Blog, SportsXP

#----- Views used for when the user has been logged in ------#


#-----stuff to make dynamic progress bar work----------------#
sports_list = {
    'Basketball': ['basketball', 0],
    'Cross Training': ['cross_training', 0],
    'Cardio': ['cardio', 0],
    'Strength Training': ['strength_training', 0],
    'Climbing': ['climbing', 0],
    'Soccer': ['soccer', 0],
    'American Football': ['american_football', 0],
    'Dance': ['dance', 0],
    'Gymnastics': ['gymnastics', 0],
    'Hiking': ['hiking', 0],
    'Swimming': ['swimming', 0],
    'Yoga': ['yoga', 0]
}

#-------------dynamic progress bar end-----------------------#


@login_required(login_url='exercise:login')
def home(request):
    '''
    Method to render the homepage (dashboard) of the user
    '''
    update_xp(request)
    context = {'sports': sports_list}
    return render(request, 'exercise/home.html', context)


@login_required(login_url='exercise:login')
def first_login(request):
    '''
    Method to save the data from first time users
    '''
    if request.method == 'POST':
        user = User.objects.get(pk=User.objects.get(
            username=request.user.get_username()).pk)       # Grabs user based on the id
        user.profile.first_login = False        # Updates the first login
        user.profile.bio = request.POST.get('bio')      # Updates the bio field
        user.save()     # Saves the data
        return HttpResponseRedirect(reverse('exercise:home'))

    context = {}
    return render(request, 'exercise/firstlogin.html', context)


@login_required(login_url='exercise:login')
def blog_post(request):
    '''
    Method to save items from a blog post
    '''
    try:
        now = datetime.datetime.now()
        blog = Blog(blog_post=request.POST['blog'],
                    blog_user=request.user.get_username(),
                    date_published=now)      # Makes an instance of the blog

    except (KeyError):      # Error handling
        context = {'blog': Blog, 'error': "An error has occurred"}
        return render(request, 'exercise/blog.html', context)
    else:
        blog.save()     # Saves the blog to the database

    return HttpResponseRedirect(reverse('exercise:blog'))


@login_required(login_url='exercise:login')
def read_sportsxp(request):
    xp_update = update_xp(request)

    context = {'sportxplist': xp_update, 'sports': sports_list}
    return HttpResponseRedirect(reverse('exercise:home'))


@login_required(login_url='exercise:login')
def update_sportsxp(request):
    global sports_list

    print(request.POST)
    update_xp(request)

    if request.method == 'POST':
        if (request.POST.get('submit') == 'Submit'):
            user = User.objects.get(pk=User.objects.get(
                username=request.user.get_username()).pk)  # Grabs user based on the id

            for key, value in sports_list.items():
                if request.POST.get('activities') == key:
                    item_id = value[0]
                    value = getattr(user.sportsxp, value[0])

                    user.sportsxp.basketball = value + 1
                    user.sportsxp.cross_training = value + 1
                    user.sportsxp.cardio = value + 1
                    user.sportsxp.strength_training = value + 1
                    user.sportsxp.climbing = value + 1
                    user.sportsxp.soccer = value + 1
                    user.sportsxp.american_football = value + 1
                    user.sportsxp.dance = value + 1
                    user.sportsxp.gymnastics = value + 1
                    user.sportsxp.hiking = value + 1
                    user.sportsxp.swimming = value + 1
                    user.sportsxp.yoga = value + 1
                    user.sportsxp.save(update_fields=[item_id])
        elif (request.POST.get('reset') == 'Reset'):
            user = User.objects.get(pk=User.objects.get(
                username=request.user.get_username()).pk)  # Grabs user based on the id

            for key, value in sports_list.items():
                if request.POST.get('activities') == key:
                    item_id = value[0]
                    user.sportsxp.basketball = 0
                    user.sportsxp.cross_training = 0
                    user.sportsxp.cardio = 0
                    user.sportsxp.strength_training = 0
                    user.sportsxp.climbing = 0
                    user.sportsxp.soccer = 0
                    user.sportsxp.american_football = 0
                    user.sportsxp.dance = 0
                    user.sportsxp.gymnastics = 0
                    user.sportsxp.hiking = 0
                    user.sportsxp.swimming = 0
                    user.sportsxp.yoga = 0
                    user.sportsxp.save(update_fields=[item_id])
        elif (request.POST.get('resetall') == "ResetAll"):
            user = User.objects.get(pk=User.objects.get(
                username=request.user.get_username()).pk)  # Grabs user based on the id
            user.sportsxp.basketball = 0
            user.sportsxp.cross_training = 0
            user.sportsxp.cardio = 0
            user.sportsxp.strength_training = 0
            user.sportsxp.climbing = 0
            user.sportsxp.soccer = 0
            user.sportsxp.american_football = 0
            user.sportsxp.dance = 0
            user.sportsxp.gymnastics = 0
            user.sportsxp.hiking = 0
            user.sportsxp.swimming = 0
            user.sportsxp.yoga = 0
            user.sportsxp.save()

    return HttpResponseRedirect(reverse('exercise:home'))


@login_required(login_url='exercise:login')
def cardioView(request):
    context = {}
    return render(request, 'exercise/cardio.html', context)


@login_required(login_url='exercise:login')
def bodyView(request):
    context = {}
    return render(request, 'exercise/bodybuilding.html', context)


@login_required(login_url='exercise:login')
def sportView(request):
    context = {}
    return render(request, 'exercise/sport.html', context)

#------ Views that can be accessed by users that have not been authenticated ------#


def blog_display(request):
    '''
    Method to display all the blog posts possible
    '''
    blog = Blog.objects.all()       # Gets all the blog posts
    context = {'blogs': blog}       # Sets them as context into the file
    return render(request, 'exercise/blog.html', context)


def route_to_landing_or_home(request):
    '''
    Method to route the user back to their home page if logged in
    or back to the landing page if not logged in
    '''
    context = {}
    if request.user.is_authenticated:       # Check authentication
        return HttpResponseRedirect(reverse('exercise:home'))
    return render(request, 'exercise/index.html', context)


def login_user(request):
    '''
    View to handle the manual login of users who have been created

    Note: This method will sign in a user regardless of if they manually created an account or used google authentication
    '''
    if request.user.is_authenticated:  # Check authentication
        if request.user.profile.first_login:
            return HttpResponseRedirect(reverse('exercise:firstlogin'))
        return HttpResponseRedirect(reverse('exercise:home'))
    else:       # Logins in user
        if request.method == 'POST':
            username = request.POST.get('username')
            password = request.POST.get('password')
            # Calls the Django authentication method
            user = authenticate(request, username=username, password=password)

            if user is not None:        # If user exists
                login(request, user)  # Logs them in
                if user.profile.first_login:
                    return HttpResponseRedirect(reverse('exercise:firstlogin'))
                return HttpResponseRedirect(reverse('exercise:home'))
            else:       # If something went wrong
                messages.info(
                    request, 'Username OR Password is Incorrect, Please try again')     # Sets message to display

        context = {}
        # Redirects to the same page
        return render(request, 'exercise/login.html', context)


def register_user(request):
    '''
    View to handle the manual creation of a user

    Note: This method will fail if a user being created already exists
    '''
    if request.user.is_authenticated:  # Checks authentication
        return HttpResponseRedirect(reverse('exercise:home'))
    else:       # Creates a new user from the template given
        form = CreateUserForm()

        if request.method == 'POST':
            # Calls our form with the post data
            form = CreateUserForm(request.POST)

            if form.is_valid():     # Checks validity
                form.save()         # Saves the form
                # Checks for unique username status
                user = form.cleaned_data.get('username')
                messages.success(request, "User Created for " + user)
                return HttpResponseRedirect(reverse('exercise:login'))

    context = {'form': form}
    # redirects the page
    return render(request, 'exercise/register.html', context)


def logout_user(request):
    '''
    Method to logout a user

    Note: This method will logout any user regardless of if they signed in with google or not
    '''
    logout(request)     # Logs out the user
    return render(request, 'exercise/index.html')   # Redirects the page

#-----------------Views for progress bar feature-----------------------#


def update_xp(request):
    global sports_list

    user = User.objects.get(pk=User.objects.get(
        username=request.user.get_username()).pk)

    for key, value in sports_list.items():
        value_of_field = getattr(user.sportsxp, value[0])
        sports_list[key][1] = value_of_field


def sortxp(request):
    global sports_list

    print(request.POST)

    sorted_sports_list = dict(
        sorted(sports_list.items(), key=lambda e: e[1][1]))
    context = {"sports": sorted_sports_list}
    return render(request, 'exercise/home.html', context)
