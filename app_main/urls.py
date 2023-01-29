from django.urls import path

from . import views

urlpatterns = [
    path('', views.projects, name='projects'),
    path('project-create/', views.project_create, name='project_create'),
    path('project-update/<str:pk>/', views.project_update, name='project_update'),
    path('project/<str:pk>/', views.project_detail, name='project_detail'),
    path('project-delete/<str:pk>/', views.project_delete, name='project_delete'),
]
