from django.contrib.auth.forms import UserCreationForm
from django.shortcuts import render
from django.views import generic
from django.http import HttpResponseRedirect, JsonResponse, HttpResponse
from django.urls import reverse
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout, get_user_model
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from .forms import CreateUserForm
from .models import Profile, Blog, SportsXP
from .forms import CreateUserForm, ExerciseForm, BmiForm
from .models import Profile, Blog, Exercise, Bmi
from friendship.models import Friend, FriendshipRequest, Block
from isodate import parse_duration
from django.conf import settings
import datetime
import requests

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

total_xp = 0

# ----- Views used for when the user has been logged in ------#


@login_required(login_url='exercise:login')
def home(request):
    '''
    Method to render the homepage (dashboard) of the user
    '''
    if request.user.profile.first_login:
        return HttpResponseRedirect(reverse('exercise:firstlogin'))

    update_xp(request)
    all_friends = Friend.objects.friends(request.user)
    unread_friend_requests_amount = Friend.objects.unrejected_request_count(
        user=request.user)
    my_user_id = User.objects.get(
        username=request.user.get_username()).pk
    try:
        friend_requests = Friend.objects.unrejected_requests(
            user=request.user)
    except:
        friend_requests = None

    context = {'sports': sports_list, 'all_friends': all_friends,
               'number_unread_requests': unread_friend_requests_amount, 'friend_requests': friend_requests,
               'total': total_xp}
    return render(request, 'exercise/home.html', context)


@login_required(login_url='exercise:login')
def first_login(request):
    '''
    Method to save the data from first time users
    '''
    print(request.POST)
    if request.method == 'POST':
        user = User.objects.get(pk=User.objects.get(
            username=request.user.get_username()).pk)  # Grabs user based on the id
        user.first_name = request.POST.get(
            'firstname')     # Adds to first name
        user.last_name = request.POST.get('lastname')   # Adds to last name
        user.profile.first_login = False  # Updates the first login
        user.profile.bio = request.POST.get('bio')  # Updates the bio field
        user.sportsxp = SportsXP()
        user.sportsxp.save()
        user.save()  # Saves the data
        return HttpResponseRedirect(reverse('exercise:home'))

    context = {}
    return render(request, 'exercise/firstlogin.html', context)


@login_required(login_url='exercise:login')
def exercise_logging(request):
    '''
    Method to save an exercise and view previous exercises
    '''
    if request.user.profile.first_login:
        return HttpResponseRedirect(reverse('exercise:firstlogin'))

    if request.method == 'POST':
        user = User.objects.get(pk=User.objects.get(
            username=request.user.get_username()).pk)
        form = ExerciseForm(request.POST)

        if form.is_valid():
            form.instance.user = user
            form.save()
            # redirect to itself
            return HttpResponseRedirect(reverse('exercise:exerciselogging'))
    else:
        form = ExerciseForm()
        # Gets all the logged exercises of a user
        exercise = Exercise.objects.filter(user=request.user)
        # Gets all the friends of a user
        all_friends = Friend.objects.friends(request.user)
        # Gets all the exercises of user's friends
        friend_exercises = Exercise.objects.filter(user__in=all_friends)

        context = {'form': form, 'exercises': exercise,
                   'friend_exercises': friend_exercises}
        return render(request, 'exercise/exercise_logging_form.html', context)


@login_required(login_url='exercise:login')
def blog_post(request):
    '''
    Method to save items from a blog post
    '''
    if request.user.profile.first_login:
        return HttpResponseRedirect(reverse('exercise:firstlogin'))
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


@login_required(login_url='exercise:login')
def read_sportsxp(request):
    if request.user.profile.first_login:
        return HttpResponseRedirect(reverse('exercise:firstlogin'))

    xp_update = update_xp(request)

    context = {'sportxplist': xp_update,
               'sports': sports_list, 'total': total_xp}
    return HttpResponseRedirect(reverse('exercise:home'))


@login_required(login_url='exercise:login')
def sport_redirect(request):
    if request.user.profile.first_login:
        return HttpResponseRedirect(reverse('exercise:firstlogin'))
    context = {}
    return render(request, 'exercise/instruction.html', context)


@login_required(login_url='exercise:login')
def friendship(request):
    if request.user.profile.first_login:
        return HttpResponseRedirect(reverse('exercise:firstlogin'))

    all_friends = Friend.objects.friends(request.user)
    unread_friend_requests_amount = Friend.objects.unrejected_request_count(
        user=request.user)
    my_user_id = User.objects.get(
        username=request.user.get_username()).pk
    try:
        friend_requests = Friend.objects.filter().exlude(user__in=all_friends)
    except:
        friend_requests = None

    context = {'sports': sports_list, 'all_friends': all_friends,
               'number_unread_requests': unread_friend_requests_amount, 'friend_requests': friend_requests,
               'total': total_xp}
    return render(request, 'exercise/friendship.html', context)


@login_required(login_url='exercise:login')
def update_sportsxp(request):
    global sports_list

    update_xp(request)

    if request.method == 'POST':
        if (request.POST.get('submit') == 'Submit'):
            for key, value in sports_list.items():
                if request.POST.get('activities') == key:
                    user = User.objects.get(pk=User.objects.get(
                        username=request.user.get_username()).pk)  # Grabs user based on the id

                    item_id = value[0]
                    value = getattr(user.sportsxp, value[0])

                    user.sportsxp.total_xp = user.sportsxp.total_xp + 1
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
                    user.sportsxp.save(
                        update_fields=[item_id, 'total_xp'])
        elif (request.POST.get('reset') == 'Reset'):
            for key, value in sports_list.items():
                if request.POST.get('activities') == key:
                    user = User.objects.get(pk=User.objects.get(
                        username=request.user.get_username()).pk)  # Grabs user based on the id
                    item_id = value[0]
                    value = getattr(user.sportsxp, value[0])

                    user.sportsxp.total_xp = user.sportsxp.total_xp - value
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
                    user.sportsxp.save(
                        update_fields=[item_id, 'total_xp'])
        elif (request.POST.get('resetall') == "Reset All"):
            user = User.objects.get(pk=User.objects.get(
                username=request.user.get_username()).pk)  # Grabs user based on the id
            for key, value in sports_list.items():
                user.sportsxp.total_xp = user.sportsxp.total_xp - \
                    getattr(user.sportsxp, value[0])

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
def bmi_display(request):
    '''
    Method to save items from a blog post
    '''
    if request.user.profile.first_login:
        return HttpResponseRedirect(reverse('exercise:firstlogin'))

    if request.method == 'POST':
        if int(request.POST.get('height_feet')) == 0 or int(request.POST.get('height_inches')) == 0:
            return HttpResponseRedirect(reverse('exercise:bmidisplay'))

        try:
            now = datetime.datetime.now()
            height_feet = int(request.POST.get('height_feet'))
            height_inches = int(request.POST.get('height_inches'))
            weight_pounds = int(request.POST.get('weight_pounds'))

            height_meters = height_feet * 0.3048 + height_inches * 0.0254
            weight_kg = weight_pounds * 0.453592
            answer = weight_kg / (height_meters * height_meters)
            answer_floored = weight_kg // (height_meters * height_meters)

            if ((answer - answer_floored) > 0.5):
                answer += 1

            bmi = Bmi(user=User.objects.get(pk=User.objects.get(
                username=request.user.get_username()).pk),
                height_feet=height_feet,
                height_inches=height_inches,
                weight_pounds=weight_pounds,
                bmi_user=request.user.get_username(),
                user_bmi=answer,
                time_of_bmi=now)  # Makes an instance of the blog

        except (KeyError):  # Error handling
            context = {'form': form, 'bmis': Bmi,
                       'error': "An error has occurred"}
            return render(request, 'exercise/bmi.html', context)
        else:
            bmi.save()  # Saves the blog to the database
            return HttpResponseRedirect(reverse('exercise:bmidisplay'))

    form = BmiForm()
    bmi = Bmi.objects.filter(user=request.user)
    context = {'form': form, 'bmis': bmi}
    return render(request, 'exercise/bmi.html', context)


@login_required(login_url='exercise:login')
def send_friend_request(request):
    sent_requests = Friend.objects.sent_requests(user=request.user)
    # rejected_list = Friend.objects.rejected_requests(user=request.user)
    friend_requested = False
    # friend_rejected = False

    for item in sent_requests:
        if (str(request.POST.get('friendusername')) == str(item.to_user)):
            friend_requested = True

    # for item in rejected_list:
    #     if (str(request.POST.get('friendusername')) == str(item.from_user)):
    #         friend_rejected = True

    if (friend_requested):
        update_xp(request)
        all_friends = Friend.objects.friends(request.user)
        unread_friend_requests_amount = Friend.objects.unrejected_request_count(
            user=request.user)
        my_user_id = User.objects.get(
            username=request.user.get_username()).pk
        try:
            friend_requests = FriendshipRequest.objects.get(
                to_user=my_user_id)
        except:
            friend_requests = None

        context = {'error': 'You already requested friendship with the user', 'sports': sports_list, 'all_friends': all_friends,
                   'number_unread_requests': unread_friend_requests_amount,
                   'total': total_xp}
        return render(request, 'exercise/friendship.html', context)

    if (str(request.user.get_username()) == str(request.POST.get('friendusername'))):
        update_xp(request)
        all_friends = Friend.objects.friends(request.user)
        unread_friend_requests_amount = Friend.objects.unrejected_request_count(
            user=request.user)
        my_user_id = User.objects.get(
            username=request.user.get_username()).pk
        try:
            friend_requests = FriendshipRequest.objects.get(
                to_user=my_user_id)
        except:
            friend_requests = None

        context = {'error': 'You cannot be friends with yourself', 'sports': sports_list, 'all_friends': all_friends,
                   'number_unread_requests': unread_friend_requests_amount,
                   'total': total_xp}
        return render(request, 'exercise/friendship.html', context)

    try:
        action_user_name_val = User.objects.get(pk=User.objects.get(
            username=request.POST.get('friendusername')).pk)

        if Friend.objects.are_friends(request.user, action_user_name_val) == True:
            update_xp(request)
            all_friends = Friend.objects.friends(request.user)
            unread_friend_requests_amount = Friend.objects.unrejected_request_count(
                user=request.user)
            my_user_id = User.objects.get(
                username=request.user.get_username()).pk
            try:
                friend_requests = FriendshipRequest.objects.get(
                    to_user=my_user_id)
            except:
                friend_requests = None

            context = {'error': 'You are already friends with the user', 'sports': sports_list, 'all_friends': all_friends,
                       'number_unread_requests': unread_friend_requests_amount, 'friend_requests': friend_requests,
                       'total': total_xp}
            return render(request, 'exercise/friendship.html', context)
    except:
        update_xp(request)
        all_friends = Friend.objects.friends(request.user)
        unread_friend_requests_amount = Friend.objects.unrejected_request_count(
            user=request.user)
        my_user_id = User.objects.get(
            username=request.user.get_username()).pk
        try:
            friend_requests = FriendshipRequest.objects.get(
                to_user=my_user_id)
        except:
            friend_requests = None

        context = {'error': 'The username entered could not be found, please try again', 'sports': sports_list, 'all_friends': all_friends,
                   'number_unread_requests': unread_friend_requests_amount,
                   'total': total_xp}
        return render(request, 'exercise/friendship.html', context)
    else:
        Friend.objects.add_friend(
            request.user,   # The sender
            action_user_name_val,   # The recipient
            message=request.POST.get('friendmessage'))

    all_friends = Friend.objects.friends(request.user)
    unread_friend_requests_amount = Friend.objects.unrejected_request_count(
        user=request.user)
    context = {'success_sent': 'Request Sent to user', 'sports': sports_list, 'all_friends': all_friends,
               'number_unread_requests': unread_friend_requests_amount,
               'total': total_xp}
    return render(request, 'exercise/friendship.html', context)


@login_required(login_url='exercise:login')
def accept_deny_block_request(request, action_user_name):
    if request.method == 'POST':
        decision = request.POST.get('Decision')
        action_user_name_val = User.objects.get(pk=User.objects.get(
            username=action_user_name).pk)
        my_user_id = User.objects.get(
            username=request.user.get_username()).pk
        action_user_id = User.objects.get(username=action_user_name_val).pk

        if decision == "Accept":
            if Friend.objects.are_friends(request.user, action_user_name_val) != True:
                friend_request = FriendshipRequest.objects.get(
                    from_user=action_user_id, to_user=my_user_id)
                friend_request.accept()
        elif decision == "Deny":
            friend_request = FriendshipRequest.objects.get(
                from_user=action_user_id, to_user=my_user_id)
            friend_request.reject()
        elif decision == "Unfriend":
            Friend.objects.remove_friend(request.user, action_user_name_val)
        elif decision == "Block":
            Block.objects.add_block(request.user, action_user_name_val)
        elif decision == "Unblock":
            Block.objects.remove_block(request.user, action_user_name_val)
    return HttpResponseRedirect(reverse('exercise:friendrequest'))


@login_required(login_url='exercise:login')
def search_youtube(request):
    if request.user.profile.first_login:
        return HttpResponseRedirect(reverse('exercise:firstlogin'))

    videos = []

    if request.method == 'POST':
        search_url = 'https://www.googleapis.com/youtube/v3/search'
        video_url = 'https://www.googleapis.com/youtube/v3/videos'

        search_params = {
            'part': 'snippet',
            'q': request.POST['search'],
            'key': settings.YOUTUBE_DATA_API_KEY,
            'maxResults': 9,
            'type': 'video'
        }

        r = requests.get(search_url, params=search_params)
        results = r.json()['items']

        video_ids = []
        for result in results:
            video_ids.append(result['id']['videoId'])

        if request.POST['submit'] == 'lucky':
            return redirect(f'https://www.youtube.com/watch?v={ video_ids[0] }')

        video_params = {
            'key': settings.YOUTUBE_DATA_API_KEY,
            'part': 'snippet,contentDetails',
            'id': ','.join(video_ids),
            'maxResults': 9
        }

        r = requests.get(video_url, params=video_params)
        results = r.json()['items']

        for result in results:
            video_data = {
                'title': result['snippet']['title'],
                'id': result['id'],
                'url': f'https://www.youtube.com/watch?v={ result["id"] }',
                'duration': int(parse_duration(result['contentDetails']['duration']).total_seconds() // 60),
                'thumbnail': result['snippet']['thumbnails']['high']['url']
            }

            videos.append(video_data)

    context = {
        'videos': videos
    }

    return render(request, 'exercise/youtube.html', context)


@login_required(login_url='exercise:login')
def cardioView(request):
    if request.user.profile.first_login:
        return HttpResponseRedirect(reverse('exercise:firstlogin'))

    context = {}
    return render(request, 'exercise/cardio.html', context)


@login_required(login_url='exercise:login')
def bodyView(request):
    if request.user.profile.first_login:
        return HttpResponseRedirect(reverse('exercise:firstlogin'))

    context = {}
    return render(request, 'exercise/bodybuilding.html', context)


@login_required(login_url='exercise:login')
def sportView(request):
    if request.user.profile.first_login:
        return HttpResponseRedirect(reverse('exercise:firstlogin'))

    context = {}
    return render(request, 'exercise/sport.html', context)


#------ Views that can be accessed by users that have not been authenticated ------#


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
                    request, 'Username OR Password is Incorrect')  # Sets message to display

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
    # Redirects the page
    return HttpResponseRedirect(reverse('exercise:landing'))

#-----------------Views for progress bar feature-----------------------#


def update_xp(request):
    global sports_list
    global total_xp

    user = User.objects.get(pk=User.objects.get(
        username=request.user.get_username()).pk)

    for key, value in sports_list.items():
        value_of_field = getattr(user.sportsxp, value[0])
        sports_list[key][1] = value_of_field

    value_of_total_xp = getattr(user.sportsxp, 'total_xp')
    total_xp = value_of_total_xp


def sortxp(request):
    global sports_list

    print(request.POST)

    sorted_sports_list = dict(
        sorted(sports_list.items(), key=lambda e: e[1][1]))
    context = {"sports": sorted_sports_list}
    return render(request, 'exercise/home.html', context)
