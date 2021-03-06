from django.urls import path

from . import views

urlpatterns = [
    path('view', views.vacview, name='vacation'),
    path('vaccreate/<str:start>/<str:end>', views.vaccreate, name='vaccreate'),
    path('vacupdate/<int:id>', views.vacupdate, name='vacupdate'),
    path('vacresize/<int:id>/<str:start>/<str:end>', views.vacresize, name='vacresize'),
    path('vacdelete/<int:id>', views.vacdelete, name='vacdelete'),
    path('vac_events.json', views.vac_events_json, name='events_json'),
    path('searchVacMonth', views.searchVacMonth, name='searchVacMonth'),
    path('vaca', views.VacataireList.as_view(), name='vacataire-list'),
    path('vacadetail/<int:pk>', views.VacataireDetail.as_view(), name='vacataire_detail'),
    path('vacaupdate/<int:pk>', views.VacataireUpdate.as_view(), name='vacataire_update'),
    path('vacadelete/<int:pk>', views.VacataireDelete.as_view(), name='vacataire_delete'),
    path('vacacreate', views.VacataireCreate.as_view(), name='vacataire_create'),
]
