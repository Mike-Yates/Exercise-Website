from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver

# Use this to create items needed for each user.
# The stuff in here will be used by all user, so you need to create it abstractly.
# The only difference is when you're saving/fetching it, you need to do it based on the username (which is unique)
# do some quick youtube video on how to save things for specific user in django an it should pop up easily.


class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    first_login = models.BooleanField(default=True)

    def __str__(self):
        return self.user.username


@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
    if created:
        Profile.objects.create(user=instance)
    instance.profile.save()


@receiver(post_save, sender=User)
def save_user_profile(sender, instance, **kwargs):
    instance.profile.save()
