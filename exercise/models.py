from django.utils import timezone
import datetime
from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver


# this is a user profile. This extends the User Model using a one-to-one link so that each User has a profile with
# fields we can customize as needed
# https://simpleisbetterthancomplex.com/tutorial/2016/07/22/how-to-extend-django-user-model.html#onetoone
class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    # these are just sample fields below, we will change these as needed
    bio = models.TextField(max_length=500, blank=True)
    location = models.CharField(max_length=30, blank=True)
    birth_date = models.DateField(null=True, blank=True)


# links creating a profile with the User model
@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
    if created:
        Profile.objects.create(user=instance)


# links saving a profile with the User model
@receiver(post_save, sender=User)
def save_user_profile(sender, instance, **kwargs):
    instance.profile.save()



# Model for the blog section
class Blog(models.Model):
    blog_post = models.TextField() # simple text field
    def __str__(self):
        return self.blog_post
