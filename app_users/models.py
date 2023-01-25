from django.db import models
from django.contrib.auth.models import User


class Profile(models.Model):
    user = models.OneToOneField(to=User, on_delete=models.CASCADE)
    fullname = models.CharField(max_length=200)
    short_intro = models.CharField(max_length=200)
    bio = models.TextField(null=True, blank=True)
    photo = models.ImageField(default='user-default.png', upload_to='profiles/', null=True, blank=True)
    skills = models.ManyToManyField(to='Skill')

    social_twitter = models.URLField(max_length=200, null=True, blank=True)
    social_instagram = models.URLField(max_length=200, null=True, blank=True)
    social_facebook = models.URLField(max_length=200, null=True, blank=True)
    social_linkedin = models.URLField(max_length=200, null=True, blank=True)
    social_telegram = models.URLField(max_length=200, null=True, blank=True)
    social_stackoverflow = models.URLField(max_length=200, null=True, blank=True)
    social_github = models.URLField(max_length=200, null=True, blank=True)
    social_website = models.URLField(max_length=200, null=True, blank=True)

    def __str__(self):
        return f'{self.user.username} - {self.fullname}'


class Skill(models.Model):
    name = models.CharField(max_length=200, unique=True)

    def __str__(self):
        return self.name
