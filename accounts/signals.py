from django.db.models.signals import post_save
from django.contrib.auth.models import User
from django.dispatch import receiver
from .models import Profile


@receiver(post_save, sender=User)
def create_or_save_user_profile(sender, instance, created, **kwargs):
    """
    Signal receiver to automatically create a Profile whenever a User is created,
    and save the profile when the User is updated.
    """
    if created:
        Profile.objects.create(user=instance)
    else:
        # Check if profile exists; if not (e.g. legacy or test fixture), create one
        if hasattr(instance, 'profile'):
            instance.profile.save()
        else:
            Profile.objects.create(user=instance)
