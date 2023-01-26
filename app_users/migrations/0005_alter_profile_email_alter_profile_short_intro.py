# Generated by Django 4.1.5 on 2023-01-25 21:54

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app_users', '0004_alter_profile_skills'),
    ]

    operations = [
        migrations.AlterField(
            model_name='profile',
            name='email',
            field=models.EmailField(blank=True, max_length=200, null=True),
        ),
        migrations.AlterField(
            model_name='profile',
            name='short_intro',
            field=models.CharField(blank=True, max_length=200, null=True),
        ),
    ]
