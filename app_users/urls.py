from django.urls import path

from . import views

urlpatterns = [
    path('', views.developers, name='developers'),

    path('account/', views.UserAccountView.as_view(), name='account'),
    path('update-account/', views.user_account_update, name='update_account'),

    path('create-skill/', views.SkillCreateView.as_view(), name='create_skill'),
    path('update-skill/<str:pk>/', views.SkillUpdateView.as_view(), name='update_skill'),
    path('delete-skill/<str:pk>/', views.skill_delete, name='delete_skill'),

    path('login/', views.user_login, name='login'),
    path('registration/', views.user_registration, name='registration'),
    path('logout/', views.user_logout, name='logout'),
]
