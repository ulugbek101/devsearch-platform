# Generated by Django 4.1.5 on 2023-02-04 03:18

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import uuid


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Profile',
            fields=[
                ('fullname', models.CharField(blank=True, max_length=200, null=True)),
                ('email', models.EmailField(blank=True, max_length=200, null=True)),
                ('short_intro', models.CharField(blank=True, max_length=200, null=True)),
                ('location', models.CharField(blank=True, max_length=200, null=True)),
                ('bio', models.TextField(blank=True, null=True)),
                ('photo', models.ImageField(blank=True, default='user-default.png', null=True, upload_to='profiles/')),
                ('social_twitter', models.URLField(blank=True, null=True)),
                ('social_instagram', models.URLField(blank=True, null=True)),
                ('social_facebook', models.URLField(blank=True, null=True)),
                ('social_linkedin', models.URLField(blank=True, null=True)),
                ('social_telegram', models.URLField(blank=True, null=True)),
                ('social_stackoverflow', models.URLField(blank=True, null=True)),
                ('social_github', models.URLField(blank=True, null=True)),
                ('social_website', models.URLField(blank=True, null=True)),
                ('social_youtube', models.URLField(blank=True, null=True)),
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False, unique=True)),
                ('created', models.DateTimeField(auto_now_add=True)),
                ('updated', models.DateTimeField(auto_now=True)),
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='Message',
            fields=[
                ('email', models.EmailField(blank=True, max_length=200, null=True)),
                ('fullname', models.CharField(blank=True, max_length=200, null=True)),
                ('subject', models.CharField(max_length=200)),
                ('body', models.TextField()),
                ('is_read', models.BooleanField(default=False)),
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False, unique=True)),
                ('created', models.DateTimeField(auto_now_add=True)),
                ('updated', models.DateTimeField(auto_now=True)),
                ('recipient', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='messages', to='app_users.profile')),
                ('sender', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='app_users.profile')),
            ],
            options={
                'verbose_name': 'Message',
                'verbose_name_plural': 'Messages',
                'ordering': ('is_read', '-created', 'subject'),
            },
        ),
        migrations.CreateModel(
            name='Skill',
            fields=[
                ('name', models.CharField(max_length=200)),
                ('description', models.TextField(blank=True, null=True)),
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False, unique=True)),
                ('created', models.DateTimeField(auto_now_add=True)),
                ('updated', models.DateTimeField(auto_now=True)),
                ('owner', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='app_users.profile')),
            ],
            options={
                'unique_together': {('owner', 'name')},
            },
        ),
    ]
