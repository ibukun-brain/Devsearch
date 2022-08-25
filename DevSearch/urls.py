"""DevSearch URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from re import template
from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from django.contrib.auth.views import (PasswordResetDoneView, PasswordResetView, 
                                    PasswordResetConfirmView, 
                                    PasswordResetCompleteView)


urlpatterns = [
    path('admin/', admin.site.urls),
    path('projects/', include('projects.urls', namespace='projects')),
    path('', include('accounts.urls', namespace='accounts')),
    path('accounts/password-reset/', 
    PasswordResetView.as_view(template_name="accounts/forget_password.html"), 
    name='password_reset'),
    path('accounts/password-reset-sent/', 
    PasswordResetDoneView.as_view(template_name='accounts/reset_password_sent.html'), 
    name="password_reset_done"),
    path('accounts/password-reset-confirm/<uidb64>/<token>/', 
    PasswordResetConfirmView.as_view(template_name='accounts/reset_password_confirm.html'), 
    name="password_reset_confirm"),
    path('accounts/password-reset-complete/', 
    PasswordResetCompleteView.as_view(template_name="accounts/reset_password_complete"), 
    name='password_reset_complete'),
    path('api/', include('api.urls'))
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)

    extra_patterns = [
    path('__debug__/', include('debug_toolbar.urls')),
    ]
    urlpatterns += extra_patterns