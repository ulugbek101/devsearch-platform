from django.urls import path

from . import views

urlpatterns = [
    path('add-tag/', views.add_tag),
    path('remove-tag/', views.remove_tag),
]
