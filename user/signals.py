from django.contrib.auth.models import User
from django.db.models.signals import post_save, pre_delete
from .models import Profile
from django.dispatch import receiver

# @receiver(post_save, sender=User)
def create_profile(sender, created, instance, *args, **kwargs):
    if created:
        Profile(user=instance, first_name=instance.username).save()


post_save.connect(create_profile, sender=User)
