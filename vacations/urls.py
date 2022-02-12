from django.urls import path

from . import views

urlpatterns = [
    path('view', views.vacview, name='vacation'),
    path('create/<str:start>/<str:end>', views.create, name='create'),
    path('events.json', views.events_json, name='events_json')
]
