from django.contrib.auth.forms import UserCreationForm
from django.shortcuts import render
from django.views import generic
from django.http import HttpResponseRedirect
from django.urls import reverse
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from .forms import CreateUserForm
from .models import Profile, Blog

#----- Views used for when the user has been logged in ------#


@login_required(login_url='login')
def home(request):
    context = {}
    return render(request, 'exercise/home.html', context)


@login_required(login_url='login')
def first_login(request):
    context = {}
    return render(request, 'exercise/firstlogin.html', context)


#------ Views that can be accessed by users that have not been authenticated ------#


def login_user(request):
    '''
    View to handle the manual login of users who have been created

    Note: This method will sign in a user regardless of if they manually created an account or used google authentication
    '''
    if request.user.is_authenticated:       # Check authentication
        return HttpResponseRedirect(reverse('exercise:home'))
    else:       # Logins in user
        if request.method == 'POST':
            username = request.POST.get('username')
            password = request.POST.get('password')
            # Calls the Django authentication method
            user = authenticate(request, username=username, password=password)

            if user is not None:        # If user exists
                login(request, user)        # Logs them in
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


# ----- Blog stuff ---



def blogDisplay(request):
    blog = Blog.objects.all()
    return render(request, 'exercise/blog.html', {'blogs': blog})



def thot(request):
    print('--------------------------------------HELLOOOO------------------')
    print(request.user.get_username())
    try:

        blog = Blog(blog_post=request.POST['blog'], blog_user=request.user.get_username())

    except(KeyError):
        return render(request, 'exercise.blog.html',{
            'blogs': Blog
        })
    else:
        blog.save()


    return HttpResponseRedirect('/exercise/blog/')

