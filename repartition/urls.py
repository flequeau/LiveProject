from django.urls import path

from . import views

urlpatterns = [
    path('export', views.export.as_view(), name='export'),
    path('addrepart', views.repartadd, name='repartadd'),
    path('view', views.repartview, name='repart'),
    path('listrepart', views.RepartList.as_view, name='repartlist'),
    path('events.json', views.events_json, name='events.json'),
    path('repupdate/<int:pk>', views.RepartUpdate.as_view(), name='repupdate'),
    path('repartupdate/<int:pk>', views.repartupdate, name='repartupdate'),
    path('repdetail/<int:pk>', views.RepartDetail.as_view(), name='repdetail'),
    path('repdelete/<int:id>', views.repartdelete, name='repartdelete'),
    path('repcreate/<str:start>/<str:end>', views.repartcreate, name='repartcreate'),
    path('linerepartcreate/<int:pk>', views.LineRepartCreate, name='linerepartcreate'),
    path('lineupdate/<int:pk>', views.lineupdate, name='lineupdate'),
    path('lineapmupdate/<int:pk>', views.lineapmupdate, name='lineapmupdate'),
    path('csmatinupdate/<int:pk>', views.csmatinupdate, name='csmatinupdate'),
    path('csapmupdate/<int:pk>', views.csapmupdate, name='csapmupdate'),

]
