import uuid
from django.db import models
from django.urls import reverse

from app_users.models import Profile


class Project(models.Model):
    owner = models.ForeignKey(to=Profile, on_delete=models.CASCADE)
    name = models.CharField(max_length=200)
    description = models.TextField(null=True, blank=True)
    photo = models.ImageField(default='project-default.jpg', upload_to='projects/')
    demo_link = models.URLField(max_length=2000, null=True, blank=True)
    source_link = models.URLField(max_length=2000, null=True, blank=True)
    tags = models.ManyToManyField(to='Tag', null=True, blank=True)
    id = models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, unique=True)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse('project', kwargs={'pk': self.id})

    @property
    def comments_count(self):
        return self.review_set.all().count()

    class Meta:
        ordering = ('-created',)


class Tag(models.Model):
    name = models.CharField(max_length=200)
    id = models.UUIDField(default=uuid.uuid4, unique=True, editable=False, primary_key=True)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name


class Review(models.Model):
    owner = models.ForeignKey(to=Profile, on_delete=models.SET_NULL, null=True)
    project = models.ForeignKey(to=Project, on_delete=models.CASCADE)
    text = models.TextField(null=True, blank=True)
    id = models.UUIDField(default=uuid.uuid4, unique=True, editable=False, primary_key=True)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f'{self.owner.fullname} - {self.project}'

    class Meta:
        ordering = ('created',)


# class Vote(models.Model):
#     VOTE_TYPE = (
#         (1, 'Like'),
#         (0, 'Dislike')
#     )
#     profile = models.ForeignKey(to=Profile, on_delete=models.CASCADE)
#     project = models.ForeignKey(to=Project, on_delete=models.CASCADE)
#     vote = models.IntegerField(choices=VOTE_TYPE, null=True, blank=True)
#
#     class Meta:
#         unique_together = ('profile', 'project')
#
#     def __str__(self):
#         return f'{self.vote} -- {self.project.title} -- {self.profile.fullname}'
