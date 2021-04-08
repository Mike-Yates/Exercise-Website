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
    height = models.IntegerField(default=0)   # for bmi calculation, should add text to specify height in inches
    weight = models.IntegerField(default=0)   # for bmi calculation, should add text to specify weight in pounds
    bmi = models.IntegerField(default=0)

    def calculate_bmi(self):
        '''
        Calculate the bmi of the user.
        BMI = weight (kg) / height^2 (meters)
        We are assuming that weight was given in pounds, and height was given in inches
        consider adjusting this later to ask for height, but give two text fields, one for feet one for inches
        '''
        weightKg = self.weight * 0.453592
        heightM = self.height * 0.0254
        bmi = weightKg / (heightM * heightM)
        return bmi

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
