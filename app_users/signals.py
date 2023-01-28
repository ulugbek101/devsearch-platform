from django.db.models.signals import post_save, post_delete
from django.dispatch import receiver
from django.contrib.auth.models import User
from .models import Profile


@receiver(signal=post_save, sender=User)
def profile_create_on_user_create(sender, instance, created, **kwargs):
    if created:
        profile = Profile.objects.create(
            user=instance,
            fullname=f'{instance.first_name} {instance.last_name}' if instance.first_name.strip() != '' and instance.last_name.strip() != '' else '',
            email=instance.email,
        )
        profile.save()


@receiver(signal=post_save, sender=Profile)
def user_change_on_profile_change(sender, instance, created, **kwargs):
    if not created:
        email = instance.email
        if email:
            instance.user.email = instance.email
            instance.user.save()


@receiver(signal=post_delete, sender=Profile)
def user_delete_on_profile_delete(sender, instance, **kwargs):
    try:
        user = instance.user
        user.delete()
    except:
        pass
