"""ios URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.8/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Add an import:  from blog import urls as blog_urls
    2. Add a URL to urlpatterns:  url(r'^blog/', include(blog_urls))
"""
from django.conf.urls import include, url
from django.contrib import admin

from . import views

urlpatterns = [
    url(r'^register_user/', views.register_user),
    url(r'^login/', views.login),
    url(r'^change_pass/', views.change_pass),
    url(r'^send_email/', views.send_email),
    url(r'^add_user/', views.add_user), 
    url(r'^reg_question/', views.add_question),
    url(r'^fast_question/', views.add_fast),
    url(r'^get_question/', views.get_question), 
    url(r'^get_fast/', views.get_fast),
    url(r'^add_score/', views.add_score),
    url(r'^get_user_data/', views.get_user_data), 
    url(r'^get_high_scores/', views.get_high_scores),
    url(r'^delete/', views.delete),
    url(r'^delete_user/',views.delete_user), 
    url(r'^/', views.index),
    url(r'^admin/', include(admin.site.urls)),
]
