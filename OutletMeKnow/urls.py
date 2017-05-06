"""OutletMeKnow URL Configuration

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
from django.conf.urls import url, include
from django.views.generic import TemplateView
from django.contrib import admin
import notifier.views
import debug_toolbar

urlpatterns = [
    url(r'^admin/', admin.site.urls),
    url(r'^status/', notifier.views.status),
    url(r'^show_all/', notifier.views.show_all),
    url(r'^about/', TemplateView.as_view(template_name='notifier/about.html')),
    url(r'^thanks/', notifier.views.thanks),
    url(r'^notification/(?P<uuid>[0-9a-f-]+)', notifier.views.visit),
    url(r'^$', notifier.views.request_notification),
    url(r'^__debug__/', include(debug_toolbar.urls)),
]