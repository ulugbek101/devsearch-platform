import uuid
from django.db import models
from django.contrib.auth.models import User


class Profile(models.Model):
    user = models.OneToOneField(to=User, on_delete=models.CASCADE)
    fullname = models.CharField(max_length=200, null=True, blank=True)
    email = models.EmailField(max_length=200, null=True, blank=True)
    short_intro = models.CharField(max_length=200, null=True, blank=True)
    location = models.CharField(max_length=200, null=True, blank=True)
    bio = models.TextField(null=True, blank=True)
    photo = models.ImageField(default='profiles/user-default.png', upload_to='profiles/', null=True, blank=True)
    social_twitter = models.URLField(max_length=200, null=True, blank=True)
    social_instagram = models.URLField(max_length=200, null=True, blank=True)
    social_facebook = models.URLField(max_length=200, null=True, blank=True)
    social_linkedin = models.URLField(max_length=200, null=True, blank=True)
    social_telegram = models.URLField(max_length=200, null=True, blank=True)
    social_stackoverflow = models.URLField(max_length=200, null=True, blank=True)
    social_github = models.URLField(max_length=200, null=True, blank=True)
    social_website = models.URLField(max_length=200, null=True, blank=True)
    social_youtube = models.URLField(max_length=200, null=True, blank=True)
    id = models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, unique=True)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    @property
    def get_fullname(self):
        if len(self.fullname.strip()) > 0:
            return self.fullname
        return self.user.username

    def __str__(self):
        return f'{self.user.username} - {self.fullname}'


class Skill(models.Model):
    owner = models.ForeignKey(to=Profile, on_delete=models.CASCADE, null=True)
    name = models.CharField(max_length=200)
    description = models.TextField(null=True, blank=True)
    id = models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, unique=True)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name

    class Meta:
        unique_together = [
            ['owner', 'name']
        ]


class Message(models.Model):
    sender = models.ForeignKey(to=Profile, on_delete=models.SET_NULL, null=True)
    recipient = models.ForeignKey(to=Profile, on_delete=models.CASCADE, related_name='messages')
    email = models.EmailField(null=True, max_length=200, blank=True)
    fullname = models.CharField(null=True, max_length=200, blank=True)
    subject = models.CharField(max_length=200)
    body = models.TextField()
    is_read = models.BooleanField(default=False)

    id = models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, unique=True)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f'{self.fullname} - {self.recipient.fullname}'

    class Meta:
        verbose_name = 'Message'
        verbose_name_plural = 'Messages'
        ordering = ('is_read', '-created', 'subject')
