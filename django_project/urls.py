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
from django.contrib.staticfiles.urls import staticfiles_urlpatterns
from django.urls import path, include, re_path
from django.views.decorators.csrf import csrf_exempt
# from cv.views import face_video, fall_down_video, fire_detection
from event_info.views import create_event, get_all_events, get_event, update_event, delete_event, \
    get_event_by_oldperson_id, get_event_by_event_date, get_event_by_event_type_and_oldperson_id, \
    get_number, get_newest_event
from sys_user.views import login_view, get_all_users, change_password
from oldperson_info import views as old_person_views
from employee_info import views as employee_views
# from videostream.consumers import VideoConsumer
# from videostream.views import camera_view, client_js, offer_view, awaitable_offer_view
from volunteer_info import views as volunteer_views

# websocket_urlpatterns = [
#     re_path(r'offer/$', VideoConsumer.as_asgi()),
# ]


urlpatterns = [
    # # path('offer/', csrf_exempt(offer_view), name='offer'),
    # path('client.js', client_js, name='client_js'),
    # path('/camera', camera_view, name='camera'),
    # path('cv/face_video/', face_video, name='face_video'),
    # path('cv/fall_down/', fall_down_video, name='fall_down_video'),
    # path('cv/fire_detection/', fire_detection, name='fire_detection'),
    # path('cv/face/', face_cv, name='face_cv'),
    path('laotoule/login/', login_view, name='login'),
    path('laotoule/users/', get_all_users, name='get_all_users'),
    path('laotoule/change_password/', change_password, name='change_password'),
    path('oldPerson/', include([
        path('create/', old_person_views.create_old_person, name='create_old_person'),
        path('get_all/', old_person_views.get_all_old_persons, name='get_all_old_persons'),
        path('get/<int:old_person_id>/', old_person_views.get_old_person, name='get_old_person'),
        path('update/<int:old_person_id>/', old_person_views.update_old_person, name='update_old_person'),
        path('delete/<int:old_person_id>/', old_person_views.delete_old_person, name='delete_old_person'),
        path('get_number/', old_person_views.get_number, name='get_number')
    ])),
    path('employee/', include([
        path('create/', employee_views.create_employee, name='create_employee'),
        path('get_all/', employee_views.get_all_employees, name='get_all_employees'),
        path('get/<int:employee_id>/', employee_views.get_employee, name='get_employee'),
        path('update/<int:employee_id>/', employee_views.update_employee, name='update_employee'),
        path('delete/<int:employee_id>/', employee_views.delete_employee, name='delete_employee'),
        path('get_number/', employee_views.get_number, name='get_number')
    ])),
    path('volunteer/', include([
        path('create/', volunteer_views.create_volunteer, name='create_volunteer'),
        path('get_all/', volunteer_views.get_all_volunteers, name='get_all_volunteers'),
        path('get/<int:volunteer_id>/', volunteer_views.get_volunteer, name='get_volunteer'),
        path('update/<int:volunteer_id>/', volunteer_views.update_volunteer, name='update_volunteer'),
        path('delete/<int:volunteer_id>/', volunteer_views.delete_volunteer, name='delete_volunteer'),
        path('get_number/', volunteer_views.get_number, name='get_number')
    ])),
    path('event/', include([
        path('create/', create_event, name='create_event'),
        path('get_all/', get_all_events, name='get_all_events'),
        path('get_event_by_oldperson_id/<int:old_person_id>/', get_event_by_oldperson_id, name='get_event_by_oldperson_id'),
        path('get_event_by_event_type/<int:event_type>/', get_event_by_oldperson_id, name='get_event_by_event_type'),
        path('get_event_by_event_type_and_oldperson_id/<int:event_type>/<int:old_person_id>/', get_event_by_event_type_and_oldperson_id, name='get_event_by_event_type_and_oldperson_id'),
        path('get_event_by_event_date/<str:event_date>/', get_event_by_event_date, name='get_event_by_event_date'),
        path('get/<int:event_id>/', get_event, name='get_event'),
        path('update/<int:event_id>/', update_event, name='update_event'),
        path('delete/<int:event_id>/', delete_event, name='delete_event'),
        path('get_number/', get_number, name='get_number'),
        path('get_newest/', get_newest_event, name='get_newest_event')
    ])),
    # re_path(r'', include(websocket_urlpatterns)),
]

urlpatterns += staticfiles_urlpatterns()
