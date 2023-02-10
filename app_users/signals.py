from django.db.models.signals import post_save, post_delete
from django.dispatch import receiver
from django.contrib.auth.models import User
from django.core.mail import send_mail
from django.conf import settings

from .models import Profile



@receiver(signal=post_save, sender=User)
def profile_create_on_user_create(sender, instance, created, **kwargs):
    if created:
        profile = Profile.objects.create(
            user=instance,
            fullname=f'{instance.first_name} {instance.last_name}' if instance.first_name.strip() and instance.last_name else '',
            email=instance.email,
        )
        profile.save()

        subject = 'Welcome to DevSearch!'
        message = 'We are glad to see you there'
        send_mail(
            subject=subject,
            message=message,
            from_email=settings.EMAIL_HOST_USER,
            recipient_list=[profile.email],
            fail_silently=True,
        )


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
