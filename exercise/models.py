from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.utils import timezone


class Profile(models.Model):
    '''
    Profile model

    Note: This is user specific and needs a user to be accessed.  
    '''
    user = models.OneToOneField(
        User, on_delete=models.CASCADE)  # Ties the info to the user
    # Info to see if this is the users first time logging in
    first_login = models.BooleanField(default=True)
    bio = models.TextField(default="")

    def __str__(self):
        return self.user.username


class SportsXP(models.Model):
    '''
    Sports model to use for the sports XP bar
    '''
    user = models.OneToOneField(
        User, on_delete=models.CASCADE)     # Ties the info to the user
    basketball = models.PositiveIntegerField(default=0)
    cross_training = models.PositiveIntegerField(default=0)
    cardio = models.PositiveIntegerField(default=0)
    strength_training = models.PositiveIntegerField(default=0)
    climbing = models.PositiveIntegerField(default=0)
    soccer = models.PositiveIntegerField(default=0)
    american_football = models.PositiveIntegerField(default=0)
    dance = models.PositiveIntegerField(default=0)
    gymnastics = models.PositiveIntegerField(default=0)
    hiking = models.PositiveIntegerField(default=0)
    swimming = models.PositiveIntegerField(default=0)
    yoga = models.PositiveIntegerField(default=0)

    def __str__(self):
        return '%s %s %s %s %s %s %s %s %s %s %s %s %s' % (self.basketball, self.cross_training, self.cardio,
                                                           self.strength_training, self.climbing, self.soccer,
                                                           self.american_football, self.dance, self.gymnastics,
                                                           self.hiking, self.swimming, self.yoga)


class Blog(models.Model):
    '''
    Blog model

    Note: Not user specific. This is just for the blog page. 
    '''
    blog_post = models.CharField(default="", max_length=500)
    blog_user = models.CharField(default="", max_length=200)
    date_published = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return self.blog_user


class Exercise(models.Model):
    '''
    Exercise model
    User specific. Logs their exercises
    '''
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    exercise_name = models.CharField(max_length=200, default="")
    reps = models.PositiveIntegerField(default=0)
    sets = models.PositiveIntegerField(default=0)
    weight_in_pounds = models.PositiveIntegerField(default=0)
    timestamp = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return self.exercise_name


@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
    if created:
        Profile.objects.create(user=instance)
    instance.profile.save()


@receiver(post_save, sender=User)
def save_user_profile(sender, instance, **kwargs):
    instance.profile.save()
