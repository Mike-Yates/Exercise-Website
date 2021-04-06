from django.shortcuts import render
from django.views import generic

from django.shortcuts import render
from django.views import generic
from django.http import *
from .models import Blog

def google_login(request):
    if request.user.is_authenticated:
        return HttpResponseRedirect('/home')
    else:
        return render(request, 'exercise/index.html')


# view that redirects first time users to a form and renders the homepage for already registered users
def home(request):
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


# Not yet implemented
class runningView(generic.TemplateView):
    template_name = 'exercise/schedule.html'

class bigView(generic.TemplateView):
    template_name = 'exercise/schedule2.html'

class sportView(generic.TemplateView):
    template_name = 'exercise/schedule3.html'

class fakeHome(generic.TemplateView):
    template_name = 'exercise/fake.html'


def blogDisplay(request):
    blog = Blog.objects.all()
    return render(request, 'exercise/blog.html', {'blogs': blog})



def thot(request):
    try:
        blog = Blog(blog_post=request.POST['blog'])
    except(KeyError):
        return render(request, 'exercise.blog.html',{
            'blogs': Blog
        })
    else:
        blog.save()

    return HttpResponseRedirect('/exercise/blog/')
