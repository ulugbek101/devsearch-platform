from django.db.models.signals import post_save, post_delete
from django.contrib.auth.models import User
from .models import Profile


def profile_create_on_user_create(sender, instance, created, **kwargs):
    if created:
        profile = Profile.objects.create(
            user=instance,
            fullname=f'{instance.first_name} {instance.last_name}' if instance.first_name.strip() != '' and instance.last_name.strip() != '' else '',
            email=instance.email,
        )
        profile.save()


def user_change_on_profile_change(sender, instance, created, **kwargs):
    if not created:
        try:
            user = instance.user
            user.email = instance.email
            user.save()
        except:
            pass


def user_delete_on_profile_delete(sender, instance, **kwargs):
    try:
        user = instance.user
        user.delete()
    except:
        pass


post_delete.connect(receiver=user_delete_on_profile_delete, sender=Profile)
post_save.connect(receiver=profile_create_on_user_create, sender=User)
post_save.connect(receiver=user_change_on_profile_change, sender=Profile)
