from django.contrib import admin

from . import models

admin.site.register(models.Profile)
admin.site.register(models.Skill)
admin.site.register(models.Message)
