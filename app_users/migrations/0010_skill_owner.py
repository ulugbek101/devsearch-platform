# Generated by Django 4.1.5 on 2023-01-26 21:15

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('app_users', '0009_skill_description'),
    ]

    operations = [
        migrations.AddField(
            model_name='skill',
            name='owner',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='app_users.profile'),
        ),
    ]
