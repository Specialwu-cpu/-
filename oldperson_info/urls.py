from django.urls import path

from oldperson_info import views

app_name = 'oldperson_info'

urlpatterns = [
    path('add/', views.create_old_person, name='create_old_person'),
    path('get/', views.get_old_person, name='get_old_person'),
    path('update/', views.update_old_person, name='update_old_person'),
    path('delete/', views.delete_old_person, name='delete_old_person'),
]
