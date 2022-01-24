from django.urls import path
from . import views

urlpatterns = [
    path('view', views.vacview, name='vacation'),
]
