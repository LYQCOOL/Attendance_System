"""Attendance_System URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.0/topics/http/urls/
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
from django.contrib import admin
from django.urls import path,include,re_path
from user import views
from django.conf.urls import url
urlpatterns = [
    path('admin/', admin.site.urls),
    path('login.html/',views.login),
    path('register.html/',views.register),
    path('check_code.html/',views.check_code),
    # path('check/',views.check),
    path('classroom/',views.classroom),
    # re_path('information/(?P<nid>\d+)/',views.information),
    path('information/basic_document/',views.information),
    re_path('viewroom/(?P<nid>\d+)/',views.viewroom),
    path('logout/',views.logout),
    path('information/basic/',views.basic_change),
    path('information/password/',views.password),
    re_path('classroom/list/(?P<nid>\d+)',views.list),
    path('order/',views.order)



]