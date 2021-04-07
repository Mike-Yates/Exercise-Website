from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver


class Profile(models.Model):
    '''
    Profile model

    Note: This is user specific and needs a user to be accessed.  
    '''
    user = models.OneToOneField(
        User, on_delete=models.CASCADE)     # Ties the info to the user
    # Info to see if this is the users first time logging in
    first_login = models.BooleanField(default=True)
    bio = models.TextField(default="")

    def __str__(self):
        return self.user.username


class Blog(models.Model):
    '''
    Blog model

    Note: Not user specific. This is just for the blog page. 
    '''
    blog_post = models.CharField(default="", max_length=500)
    blog_user = models.CharField(default="", max_length=200)
    date_published = models.DateTimeField("date published")

    def __str__(self):
        return self.blog_user


@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
    if created:
        Profile.objects.create(user=instance)
    instance.profile.save()


@receiver(post_save, sender=User)
def save_user_profile(sender, instance, **kwargs):
    instance.profile.save()
