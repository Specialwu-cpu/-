"""
URL configuration for django_project project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.2/topics/http/urls/
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
from django.urls import path, include

from sys_user.views import login_view, get_all_users, change_password
from oldperson_info import views as old_person_views
from employee_info import views as employee_views
from volunteer_info import views as volunteer_views

urlpatterns = [
    path('laotoule/login/', login_view, name='login'),
    path('laotoule/users/', get_all_users, name='get_all_users'),
    path('laotoule/change_password/', change_password, name='change_password'),
    path('oldPerson/', include([
        path('add/', old_person_views.create_old_person, name='create_old_person'),
        path('get_all/', old_person_views.get_all_old_persons, name='get_all_old_persons'),
        path('get/<int:old_person_id>/', old_person_views.get_old_person, name='get_old_person'),
        path('update/<int:old_person_id>/', old_person_views.update_old_person, name='update_old_person'),
        path('delete/<int:old_person_id>/', old_person_views.delete_old_person, name='delete_old_person'),
    ])),
    path('employee/', include([
        path('create/', employee_views.create_employee, name='create_employee'),
        path('get/<int:employee_id>/', employee_views.get_employee, name='get_employee'),
        path('update/<int:employee_id>/', employee_views.update_employee, name='update_employee'),
        path('delete/<int:employee_id>/', employee_views.delete_employee, name='delete_employee'),
    ])),
    path('volunteer/', include([
        path('create/', volunteer_views.create_volunteer, name='create_volunteer'),
        path('get/<int:volunteer_id>/', volunteer_views.get_volunteer, name='get_volunteer'),
        path('update/<int:volunteer_id>/', volunteer_views.update_volunteer, name='update_volunteer'),
        path('delete/<int:volunteer_id>/', volunteer_views.delete_volunteer, name='delete_volunteer'),
    ])),
]
