from django.urls import path

from . import views

urlpatterns = [
    path('view', views.vacview, name='vacation'),
    path('create/<str:start>/<str:end>', views.create, name='create'),
    path('update/<int:id>', views.update, name='update'),
    path('resize/<int:id>/<str:start>/<str:end>', views.resize, name='resize'),
    path('delete/<int:id>', views.delete, name='delete'),
    path('events.json', views.events_json, name='events_json')
]
