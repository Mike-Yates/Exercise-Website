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


class SportsXP(models.Model):
    '''
    Sports model to use for the sports XP bar
    '''
    user = models.OneToOneField(
        User, on_delete=models.CASCADE)     # Ties the info to the user
    last_performed_date = models.DateTimeField("date updated")
    basketball = models.IntegerField(default=0)
    cross_training = models.IntegerField(default=0)
    cardio = models.IntegerField(default=0)
    strength_training = models.IntegerField(default=0)
    climbing = models.IntegerField(default=0)
    soccer = models.IntegerField(default=0)
    american_football = models.IntegerField(default=0)
    dance = models.IntegerField(default=0)
    gymnastics = models.IntegerField(default=0)
    hiking = models.IntegerField(default=0)
    swimming = models.IntegerField(default=0)
    yoga = models.IntegerField(default=0)

    def __str__(self):
        return '%s %s %s %s %s %s %s %s %s %s %s %s %s' % (self.basketball, self.cross_training, self.cardio,
                                                           self.strength_training, self.climbing, self.soccer,
                                                           self.american_football, self.dance, self.gymnastics,
                                                           self.hiking, self.swimming, self.yoga, self.last_performed_date)


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
