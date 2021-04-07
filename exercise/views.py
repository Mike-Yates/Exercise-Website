from django.contrib.auth.forms import UserCreationForm
from django.shortcuts import render
from django.views import generic
from django.http import HttpResponseRedirect
from django.urls import reverse
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
import datetime
from .forms import CreateUserForm, ExerciseForm
from .models import Profile, Blog, Exercise


# ----- Views used for when the user has been logged in ------#


@login_required(login_url='exercise:login')
def home(request):
    '''
    Method to render the homepage (dashboard) of the user
    '''
    context = {}
    return render(request, 'exercise/home.html', context)


@login_required(login_url='exercise:login')
def first_login(request):
    '''
    Method to save the data from first time users
    '''
    if request.method == 'POST':
        user = User.objects.get(pk=User.objects.get(
            username=request.user.get_username()).pk)  # Grabs user based on the id
        user.profile.first_login = False  # Updates the first login
        user.profile.bio = request.POST.get('bio')  # Updates the bio field
        user.save()  # Saves the data
        return HttpResponseRedirect(reverse('exercise:home'))

    context = {}
    return render(request, 'exercise/firstlogin.html', context)


@login_required(login_url='exercise:login')
def exercise_logging(request):
    '''
    Method to save an exercise and view previous exercises
    '''
    if request.method == 'POST':
        user = User.objects.get(pk=User.objects.get(
            username=request.user.get_username()).pk)
        form = ExerciseForm(request.POST)

        if form.is_valid():
            form.instance.user = user
            form.save()
            return HttpResponseRedirect(reverse('exercise:exerciselogging'))  # redirect to itself
    else:
        form = ExerciseForm()
        exercise = Exercise.objects.filter(user=request.user)  # Gets all the logged exercises of a user

        return render(request, 'exercise/exercise_logging_form.html', {'form': form, 'exercises': exercise})


@login_required(login_url='exercise:login')
def blog_post(request):
    '''
    Method to save items from a blog post
    '''
    try:
        now = datetime.datetime.now()
        blog = Blog(blog_post=request.POST['blog'],
                    blog_user=request.user.get_username(),
                    date_published=now)  # Makes an instance of the blog

    except (KeyError):  # Error handling
        context = {'blog': Blog, 'error': "An error has occurred"}
        return render(request, 'exercise/blog.html', context)
    else:
        blog.save()  # Saves the blog to the database

    return HttpResponseRedirect(reverse('exercise:blog'))


# ------ Views that can be accessed by users that have not been authenticated ------#

def blog_display(request):
    '''
    Method to display all the blog posts possible
    '''
    blog = Blog.objects.all()  # Gets all the blog posts
    context = {'blogs': blog}  # Sets them as context into the file
    return render(request, 'exercise/blog.html', context)


def route_to_landing_or_home(request):
    '''
    Method to route the user back to their home page if logged in
    or back to the landing page if not logged in
    '''
    context = {}
    if request.user.is_authenticated:  # Check authentication
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
    else:  # Logins in user
        if request.method == 'POST':
            username = request.POST.get('username')
            password = request.POST.get('password')
            # Calls the Django authentication method
            user = authenticate(request, username=username, password=password)

            if user is not None:  # If user exists
                login(request, user)  # Logs them in
                if user.profile.first_login:
                    return HttpResponseRedirect(reverse('exercise:firstlogin'))
                return HttpResponseRedirect(reverse('exercise:home'))
            else:  # If something went wrong
                messages.info(
                    request, 'Username OR Password is Incorrect, Please try again')  # Sets message to display

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
    else:  # Creates a new user from the template given
        form = CreateUserForm()

        if request.method == 'POST':
            # Calls our form with the post data
            form = CreateUserForm(request.POST)

            if form.is_valid():  # Checks validity
                form.save()  # Saves the form
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
    logout(request)  # Logs out the user
    return render(request, 'exercise/index.html')  # Redirects the page

# class sportView(generic.TemplateView):
#     template_name = 'exercise/schedule3.html'


# class bigView(generic.TemplateView):
#     template_name = 'exercise/schedule2.html'


# class runningView(generic.TemplateView):
#     template_name = 'exercise/schedule.html'
