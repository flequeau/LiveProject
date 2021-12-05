from django.urls import path
from . import views

urlpatterns = [
    path('blood', views.blood, name='blood'),
]
