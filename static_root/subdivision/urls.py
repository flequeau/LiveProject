from django.urls import path
from django.views.generic import TemplateView
from subdivision import views

urlpatterns = [
    # event
    path('addevent', views.add_event, name='addevent'),
    path('view', TemplateView.as_view(template_name='subdivision/event/rempla.html'), name='rempla'),
    path('list', views.EventList.as_view(), name='event_list'),
    path('detail/<int:pk>', views.EventDetail.as_view(), name='event_detail'),
    path('events.json', views.events_json, name='events.json'),
    path('update/<int:id>', views.update, name='update'),
    path('delete/<int:id>', views.delete, name='delete'),
    path('create/<str:start>/<str:end>', views.create, name='create'),
    path('resize/<int:id>/<str:end>', views.resize, name='resize'),
    path('drop/<int:id>/<str:start>/<str:end>', views.drop, name='drop'),
    # rpt
    path('rpt', views.RptList.as_view(), name='rpt_list'),
    path('rptdetail/<int:pk>', views.RptDetail.as_view(), name='rpt_detail'),
    path('rptupdate/<int:pk>', views.RptUpdate.as_view(), name='rpt_update'),
    path('rptdelete/<int:pk>', views.RptDelete.as_view(), name='rpt_delete'),
    path('rptcreate', views.RptCreate.as_view(), name='rpt_create'),
    # pdf
    path('editpdf/<int:id>', views.edit_pdf, name='editpdf'),
    path('monthpdf/<annee>/<mois>/<items>', views.pdf_month, name='monthpdf'),
    path('searchrptmonth', views.searchrptmonth, name='searchrptmonth'),
    path('searchMonth/<message>', views.searchMonth, name='searchMonth'),
    # crud ajax rpt
    path('crud_rpt/', views.CrudView.as_view(), name='crud_ajax'),
    path('ajax/crud/create/', views.CreateCrudRpt.as_view(), name='crud_ajax_create'),
    path('ajax/crud/update/', views.UpdateCrudRpt.as_view(), name='crud_ajax_update'),
    path('ajax/crud/delete/', views.DeleteCrudRpt.as_view(), name='crud_ajax_delete'),
    path('index', views.index, name='index'),
    path('ajax_calls/search', views.autocompleteModel, name='search'),
    # are
    path('are', views.AreList.as_view(), name='are_list'),
    path('aredetail/<int:pk>', views.AreDetail.as_view(), name='are_detail'),
    path('areupdate/<int:pk>', views.AreUpdate.as_view(), name='are_update'),
    path('aredelete/<int:pk>', views.AreDelete.as_view(), name='are_delete'),
    path('arecreate', views.AreCreate.as_view(), name='are_create'),

]