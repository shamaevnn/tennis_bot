"""tennis_bot URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.11/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.conf.urls import url, include
    2. Add a URL to urlpatterns:  url(r'^blog/', include('blog.urls'))
"""
from django.conf.urls import url
from django.contrib import admin
from django.urls import path, include
from django.views.decorators.csrf import csrf_exempt

from base.views import (
    home_redirect,
    TelegramBotWebhookView,
    TelegramAdminBotWebhookView,
)

handler404 = "base.views.my_custom_page_not_found_view"
handler500 = "base.views.my_custom_error_view"

urlpatterns = [
    path("api/", include("api.urls")),
    url(r"^tgadmin/", admin.site.urls),
    url(r"^$", home_redirect, name="home"),
    path("super_secter_webhook/", csrf_exempt(TelegramBotWebhookView.as_view())),
    path(
        "super_secter_admin_webhook/",
        csrf_exempt(TelegramAdminBotWebhookView.as_view()),
    ),
]
