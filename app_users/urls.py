from django.urls import path

from . import views


urlpatterns = [
    path('', views.developers, name='developers'),

    path('account/', views.user_account, name='account'),

    path('login/', views.user_login, name='login'),
    path('registration/', views.user_registration, name='registration'),
    path('logout/', views.user_logout, name='logout'),
]