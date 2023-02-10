from django.contrib import admin
from django.urls import path, include

from django.conf import settings
from django.conf.urls.static import static

from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
)

from django.contrib.auth.views import PasswordResetView, PasswordResetDoneView, PasswordResetConfirmView, \
    PasswordResetCompleteView

urlpatterns = [
    path('admin/', admin.site.urls),

    path('projects/', include('app_main.urls')),
    path('', include('app_users.urls')),

    path('api/v1/', include('api.urls')),
    path('api/token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('api/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),

    path('password-reset/', PasswordResetView.as_view(template_name='app_users/password-reset.html'),
         name='password_reset'),
    path('password-reset-done/', PasswordResetDoneView.as_view(template_name='app_users/password-reset-done.html'),
         name='password_reset_done'),
    path('reset/<token>/<uidb64>/',
         PasswordResetConfirmView.as_view(template_name='app_users/password-reset-confirm.html'),
         name='password_reset_confirm'),
    path('password-reset-complete/',
         PasswordResetCompleteView.as_view(template_name='app_users/password-reset-complete.html'),
         name='password_reset_complete'),
]

if settings.DEBUG:
    urlpatterns += static(prefix=settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
    # urlpatterns += static(prefix=settings.STATIC_URL, document_root=settings.STATIC_ROOT)
