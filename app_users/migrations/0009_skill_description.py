# Generated by Django 4.1.5 on 2023-01-25 22:44

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app_users', '0008_profile_social_youtube'),
    ]

    operations = [
        migrations.AddField(
            model_name='skill',
            name='description',
            field=models.TextField(blank=True, null=True),
        ),
    ]
