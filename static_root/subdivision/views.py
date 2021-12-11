import json
import os
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import FileResponse, Http404, JsonResponse, HttpResponse
from django.conf import settings
from datetime import datetime, timedelta
from django.views.generic import ListView, DetailView, View
from django.views.generic.edit import CreateView, UpdateView, DeleteView, FormView
from django import http
from django.urls import reverse_lazy
from django.shortcuts import render, redirect, get_object_or_404
from django.template.loader import render_to_string
import pdfkit
from datetime import timedelta
from .forms import EventForm, SearchRptMonthForm, SearchMonthForm
from .models import Event, Calendrier, WebColor, Rpt, Are, HopParam


####### CRUD AJAX RPT ################# CRUD AJAX RPT ################# CRUD AJAX RPT ##########
class CrudView(LoginRequiredMixin, ListView):
    model = Rpt
    template_name = 'subdivision/rpt/rpt_crud.html'
    context_object_name = 'rpts'


class CreateCrudRpt(LoginRequiredMixin, View):
    def get(self, request):
        name1 = request.GET.get('name', None)
        forname1 = request.GET.get('forname', None)
        tel1 = request.GET.get('tel', None)
        email1 = request.GET.get('email', None)

        obj = Rpt.objects.create(
            name=name1,
            forname=forname1,
            telmob=tel1,
            email=email1
        )
        rpt = {'id': obj.id, 'name': obj.name, 'forname': obj.forname, 'tel': obj.telmob, 'email': obj.email}
        data = {
            'rpt': rpt
        }
        return JsonResponse(data)


class UpdateCrudRpt(LoginRequiredMixin, View):
    def get(self, request):
        id1 = request.GET.get('id', None)
        name1 = request.GET.get('name', None)
        forname1 = request.GET.get('forname', None)
        tel1 = request.GET.get('tel', None)
        email1 = request.GET.get('email', None)

        obj = Rpt.objects.get(id=id1)
        obj.name = name1
        obj.forname = forname1
        obj.telmob = tel1
        obj.email = email1
        obj.save()

        rpt = {'id': obj.id, 'name': obj.name, 'forname': obj.forname, 'tel': obj.telmob, 'email': obj.email}

        data = {
            'rpt': rpt
        }
        return JsonResponse(data)


class DeleteCrudRpt(LoginRequiredMixin, View):
    def get(self, request):
        id1 = request.GET.get('id', None)
        Rpt.objects.get(id=id1).delete()
        data = {
            'deleted': True
        }
        return JsonResponse(data)


####### PDF EDIT ################# PDF EDIT ################# PDF EDIT ##########

def edit_pdf(request, id):
    event = Event.objects.get(pk=id)
    y = event.start.year
    m = event.start.month
    if event.start == event.jend:
        findate = ''
    else:
        findate = event.jend.strftime('%d/%m%/%Y')
    date = event.start.strftime('%d/%m%/%Y')
    hop = HopParam.objects.get(pk=1)
    css = [
        settings.STATIC + '/css/bootstrap.css',
    ]

    # if settings.STATIC_ROOT + event.are.signature.url:
    # signpathare = settings.STATIC_ROOT + event.are.signature.url
    # else:
    # signpathare = ''

    if event.calendrier_id == 1:
        p = 'staticfiles/img/contrat/' + str(y) + '/' + str(m) + '/'
        url = 'subdivision/contrat.html'
    else:
        p = 'staticfiles/img/annexe/' + str(y) + '/' + str(m) + '/'
        url = 'subdivision/annexe.html'
    os.makedirs(p, exist_ok=True)
    contrat = render_to_string(url, {'are': event.are,
                                     'rpt': event.rpt,
                                     'date': date,
                                     'fdate': findate,
                                     'hop': hop,
                                     # 'signpath': signpathare,
                                     })
    path = p + event.start.strftime('%Y%m%d') + \
           event.are.name.replace(' ', '_') + '_' + event.rpt.name.replace(' ', '_') + '.pdf'
    pdfkit.from_string(contrat, path, css=css)
    return FileResponse(open(path, 'rb'), content_type='application/pdf')



def pdf_month(request, annee, mois, items):
    hop = HopParam.objects.get(pk=1)
    css = [
        settings.STATIC + '/css/bootstrap.css',
    ]
    message = ''
    listcouple = []
    events = Event.objects.filter(start__year=annee, start__month=mois).order_by('start')
    if events:
        for event in events:
            datecouple = []
            if (event.are, event.rpt) not in listcouple:
                # if settings.STATIC_ROOT + event.are.signature.url:
                # signpathare = settings.STATIC_ROOT + event.are.signature.url
                # else:
                # signpathare = ''
                listcouple.append((event.are, event.rpt))
                dates = events.filter(are=event.are, rpt=event.rpt).order_by('start')
                for date in dates:
                    d = date.start.strftime('%d/%m%/%Y')
                    if date.start == date.jend:
                        fd = ''
                    else:
                        fd = date.jend.strftime('%d/%m%/%Y')
                        d = d + ' au ' + fd
                    datecouple.append(d)
                    if event.calendrier_id == 1:
                        p = 'staticfiles/img/contrat/' + str(annee) + '/' + str(mois) + '/'
                        url = 'subdivision/contrat.html'
                    else:
                        p = 'staticfiles/img/annexe/' + str(annee) + '/' + str(mois) + '/'
                        url = 'subdivision/annexe.html'

                    os.makedirs(p, exist_ok=True)
                    dc = ', '.join(datecouple)
                    contrat = render_to_string(url, {'are': event.are,
                                                     'rpt': event.rpt,
                                                     'date': dc,
                                                     'hop': hop,
                                                     # 'signpath': signpathare,
                                                     })
                    path = p + event.start.strftime('%Y%m%d') + \
                           event.are.name.replace(' ', '_') + '_' + event.rpt.name.replace(' ', '_') + '.pdf'
                    pdfkit.from_string(contrat, path, css=css)
                    message = 'Opération terminée'
            else:
                pass
    else:
        message = 'Pas d\'édition à créer'
    return redirect('searchMonth', message=message)


MOIS = {'NC', 'Janvier', 'Février', 'Mars', 'Avril', 'Mai', 'Juin', 'Juillet', 'Août', 'Septembre', 'Octobre',
        'Novembre', 'Décembre'}



def searchrptmonth(request):
    today = datetime.now()
    anneeprev = today - timedelta(weeks=52)
    anneefin = today + timedelta(weeks=104)
    annees = [(x) for x in range(anneeprev.year, anneefin.year)]
    rpt = mois = annee = items = rpt_choice = message = ''
    rpts = Rpt.objects.all()
    if request.method == 'POST':
        rpt = request.POST.get('name')
        mois = int(request.POST.get('mois'))
        annee = int(request.POST.get('annee'))
        if Rpt.objects.filter(name=rpt):
            rpt_choice = Rpt.objects.get(name=rpt)
            print(rpt_choice)
            print(mois)
            print(annee)
            if Event.objects.filter(rpt=rpt_choice, start__month=mois, start__year=annee):
                items = Event.objects.filter(rpt=rpt_choice, start__month=mois, start__year=annee).order_by('start')
                # rpt_choice = rpt_choice.forname + ' ' + rpt_choice.name + ' (' + MOIS[mois] + ' ' + str(annee) + ')'
                rpt_choice = '{} {} ( {} {} )'.format(rpt_choice.forname, rpt_choice.name, str(mois), str(annee))
                print(rpt_choice)
                return render(request, 'subdivision/event/searchRptMonthForm.html', {'annees': annees,
                                                                                     'items': items,
                                                                                     'rpt': rpt_choice,
                                                                                     'rpts': rpts,
                                                                                     'gerant': settings.GERANT,
                                                                                     })
            else:
                message = "Pas de remplacement trouvé pour ce remplaçant durant ce mois"
        else:
            message = "Le nom du remplaçant recherché n'est pas valide."
            return render(request, 'subdivision/event/searchRptMonthForm.html', {"rpts": rpts,
                                                                                 'annees': annees,
                                                                                 'message': message})
    return render(request, 'subdivision/event/searchRptMonthForm.html', {"rpts": rpts,
                                                                         'annees': annees,
                                                                         })


####### CRUD RPT ################# CRUD RPT ################# CRUD RPT ##########
class RptList(LoginRequiredMixin, ListView):
    model = Rpt
    template_name = 'subdivision/rpt/rpt_list.html'


class RptDetail(LoginRequiredMixin, DetailView):
    model = Rpt
    template_name = 'subdivision/rpt/rpt_detail.html'


class RptUpdate(LoginRequiredMixin, UpdateView):
    model = Rpt
    fields = ['name', 'forname', 'email', 'telmob', 'adress1', 'adress2', 'town',
              'postalcode', 'tel2', 'tel3', 'status', 'rpps', 'codepartname', 'codepartnum',
              'conum', 'urssafnum', 'photo', 'sirennum', 'active', 'licence_exp_date', 'licence', 'assurance']
    template_name = 'subdivision/rpt/rpt_form.html'


class RptCreate(LoginRequiredMixin, CreateView):
    model = Rpt
    fields = ['name', 'forname', 'email', 'telmob', 'adress1', 'adress2', 'town',
              'postalcode', 'tel2', 'tel3', 'status', 'rpps', 'codepartname', 'codepartnum',
              'conum', 'urssafnum', 'photo', 'sirennum', 'active']
    template_name = 'subdivision/rpt/rpt_create.html'


class RptDelete(LoginRequiredMixin, DeleteView):
    model = Rpt
    template_name = 'subdivision/rpt/rpt_delete.html'
    success_url = reverse_lazy('rpt_list')


####### CRUD EVENT ################# CRUD EVENT ################# CRUD EVENT ##########
class EventList(LoginRequiredMixin, ListView):
    model = Event
    template_name = 'subdivision/event/event_list.html'


class EventDetail(LoginRequiredMixin, DetailView):
    model = Event
    template_name = 'subdivision/event/event_detail.html'



def add_event(request):
    """
    Formulaire de création d'un nouvel évenement. Les heures sont pré-remplies par 00:00
    :param request: aucun
    :return: un event qui s'affichera sur le calendrier
    """
    if request.method == 'POST':
        form = EventForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('addevent')
    else:
        form = EventForm(initial={'start_time': '00:00:00', 'end_time': '00:00:00'})
    return render(request, 'subdivision/event/event.html', {'form': form})



def events_json(request):
    """
    Crée le fichier json qui est lu pour être affiché sur le calendrier
    :param request: aucun
    :return: Liste des évenements sérializés en json
    anneeprev et anneepost permettent de n'afficher que les remplas de l'année précédente (pas de chargement en deça
    et ceux de l'année à venir
    """
    today = datetime.now()
    anneeprev = today - timedelta(weeks=52)
    anneepost = today + timedelta(weeks=52)
    events = Event.objects.filter(start__range=(anneeprev, anneepost))
    event_list = []

    for event in events:
        event_start = event.start
        event_end = event.end
        calendar = Calendrier.objects.get(pk=event.calendrier_id)
        webcolor = WebColor.objects.get(pk=calendar.color_id)
        event_list.append({
            'id': event.id,
            'start': event_start.strftime('%Y-%m-%d'),
            'end': event_end.strftime('%Y-%m-%d'),
            'title': event.title,
            'color': webcolor.color
        })
    if len(event_list) == 0:
        raise http.Http404
    else:
        return http.HttpResponse(json.dumps(event_list),
                                 content_type='application/json')



def update(request, id):
    """
    Récupère l'id d'un event pour updater celui-ci
    :param request: id de l'event cliqué sur le calendrier
    :param id: event choisi
    :return: le formulaire avec les données enregistrées destinées à être modifiées
    """
    event = get_object_or_404(Event, pk=id)
    if Event.objects.filter(are=event.are, rpt=event.rpt).exists():
        event_idems = Event.objects.filter(are=event.are, rpt=event.rpt, start__lt=event.start)
    else:
        event_idems = ''
    form = EventForm(request.POST or None, instance=event)
    if request.method == 'POST':
        if form.is_valid():
            instance = form.save(commit=False)
            instance.title = instance.are.name + ' - ' + instance.rpt.name
            instance.save()
            return redirect('rempla')
        else:
            message = 'Le remplacé ou le remplaçant a déjà un contrat à cette date'
            return render(request, 'subdivision/event/event_update.html', {'form': form,
                                                                           'id': id,
                                                                           'start': event.start,
                                                                           'end': event.end,
                                                                           'title': event.title,
                                                                           'type': event.type,
                                                                           'calendrier': event.calendrier,
                                                                           'message': message,
                                                                           'event_idems': event_idems,
                                                                           })
    else:
        return render(request, 'subdivision/event/event_update.html', {'form': form,
                                                                       'id': id,
                                                                       'start': event.start,
                                                                       'end': event.end,
                                                                       'title': event.title,
                                                                       'type': event.type,
                                                                       'calendrier': event.calendrier,
                                                                       'event_idems': event_idems,
                                                                       })



def delete(request, id):
    """
    Recupere l'id d'un event pour supprimer celui-ci
    :param request: id de l'event clique sur le calendrier
    :param id: event choisi
    :return: le formulaire avec les donnees enregistrees destinees a etre modifiees
    """
    event = get_object_or_404(Event, pk=id)
    event.delete()
    return redirect('rempla')



def create(request, start, end):
    """
    Creation d'un event lors d'un click dans une case du calendrier
    :param request:
    :param start: date et heure de debut de la case
    :param end: date et heure de fin de la case
    :return: si la vue est Day ou que l'heure = 00 le formulaire est prerempli avec date, sinon avec date et heure
    """
    start_event = start[4:8] + '-' + start[2:4] + '-' + start[:2]
    start_event = datetime.strptime(start_event, '%Y-%m-%d')
    end_event = end[4:8] + '-' + end[2:4] + '-' + end[:2]
    end_event = datetime.strptime(end_event, '%Y-%m-%d')
    start = start[:2] + '/' + start[2:4] + '/' + start[4:8]
    if Event.objects.filter(start=start_event).exists:
        idems = Event.objects.filter(start=start_event)
    else:
        idems = ''
    if request.method == 'POST':
        form = EventForm(request.POST)
        if form.is_valid():
            instance = form.save(commit=False)
            instance.title = instance.are.name + ' - ' + instance.rpt.name
            if Event.objects.filter(are=instance.are, rpt=instance.rpt, start__lt=instance.start).exists():
                instance.calendrier_id = 2
            else:
                instance.calendrier_id = 1
            instance.save()
            return redirect('rempla')
        else:
            message = 'Le remplacé ou le remplaçant a déjà un contrat à cette date'
            return render(request, 'subdivision/event/event.html',
                          {'form': form, 'message': message, 'idems': idems})
    else:
        form = EventForm(initial={'start': start_event, 'end': end_event})
        return render(request, 'subdivision/event/event.html', {'form': form, 'idems': idems})



def resize(request, id, end):
    """
    Modifie un event lors d'une modification de sa duree dans le calendrier
    :param request:
    :param id: l'id de l'event
    :param view: la view calendrier de l'event - Si month modification en jour -
    :param delta: la duree d'allongement de l'event en millisecondes
    :return: Modification de l'event en base de donnees et retour au calendrier
    """
    event = get_object_or_404(Event, pk=id)
    endtime = end[8:10] + ':' + end[10:12] + ':00'
    end = end[:2] + '/' + end[2:4] + '/' + end[4:8]
    end = datetime.strptime(end, '%d/%m/%Y')
    endtime = datetime.strptime(endtime, '%H:%M:%S')
    if endtime.hour == '0':
        event.end = end
        event.save()

    else:
        event.end = end
        event.end_time = endtime - timedelta(minutes=endtime.minute % 10)
        event.save()
    return redirect('rempla')



def drop(request, id, start, end):
    """
    Modifie un event lors d'un deplacement par drop
    :param request:
    :param id: id de l'event
    :param start: date et heure modifiees de start
    :param end: date et heure modifiee de end
    :return:
    """
    event = get_object_or_404(Event, pk=id)
    starttime = start[8:10] + ':' + start[10:12] + ':00'
    start = start[:2] + '/' + start[2:4] + '/' + start[4:8]
    start = datetime.strptime(start, '%d/%m/%Y')
    starttime = datetime.strptime(starttime, '%H:%M:%S')
    endtime = end[8:10] + ':' + end[10:12] + ':00'
    end = end[:2] + '/' + end[2:4] + '/' + end[4:8]
    end = datetime.strptime(end, '%d/%m/%Y')
    endtime = datetime.strptime(endtime, '%H:%M:%S')
    if endtime.hour == '0':
        event.start = start
        event.end = end
        event.save()
    else:
        event.start = start
        event.end = end
        event.start_time = starttime - timedelta(minutes=starttime.minute % 10)
        event.end_time = endtime - timedelta(minutes=endtime.minute % 10)
        event.save()
    return redirect('rempla')



def searchMonth(request, message):
    if request.method == 'POST':
        form = SearchMonthForm(request.POST)
        if form.is_valid():
            message = 'Editions des contrats et Annexes calendaires disponibles'
            annee = int(form.data['annee'])
            mois = int(form.data['mois'])
            items = Event.objects.filter(start__month=mois, start__year=annee).order_by('start')
            return render(request, 'subdivision/event/searchMonthForm.html', {'form': form,
                                                                              'items': items,
                                                                              'message': message,
                                                                              'annee': annee,
                                                                              'mois': mois})
    else:
        form = SearchMonthForm()
    return render(request, 'subdivision/event/searchMonthForm.html', {'form': form,
                                                                      'message': message
                                                                      })


####### SEARCH RPT AJAX ################# SEARCH RPT AJAX ##########
def index(request):
    today = datetime.now()
    anneeprev = today - timedelta(weeks=52)
    anneefin = today + timedelta(weeks=104)
    rpt = mois = annee = ''
    rpts = Rpt.objects.all()
    annees = [(x) for x in range(anneeprev.year, anneefin.year)]
    if request.method == 'POST':
        rpt = request.POST.get('name')
        mois = request.POST.get('mois')
        annee = request.POST.get('annee')

        if Rpt.objects.filter(name=rpt).exists:
            rpt_choice = Rpt.objects.get(name=rpt)

            return render(request, 'subdivision/rpt/index.html', {'annees': annees,
                                                                  'rpt': rpt_choice,
                                                                  })
        else:
            pass
    return render(request, 'subdivision/rpt/index.html', {"rpts": rpts,
                                                          'annees': annees})


def autocompleteModel(request):
    if request.is_ajax():
        q = request.GET.get('term')
        search_qs = Rpt.objects.filter(name__startswith=q)
        results = []
        for r in search_qs:
            results.append(r.name)
        data = json.dumps(results)
    mimetype = 'application/json'
    return HttpResponse(data, mimetype)


####### CRUD ARE ################# CRUD ARE ################# CRUD ARE ##########

class AreList(LoginRequiredMixin, ListView):
    model = Are
    template_name = 'subdivision/are/are_list.html'
    ordering = ['name']


class AreDetail(LoginRequiredMixin, DetailView):
    model = Are
    template_name = 'subdivision/are/are_detail.html'


class AreUpdate(LoginRequiredMixin, UpdateView):
    model = Are
    fields = ['name', 'forname', 'email', 'telmob', 'adress1', 'adress2', 'town',
              'postalcode', 'tel2', 'phone_hop', 'phone_secretary', 'rpps',
              'coNum', 'secteur']
    template_name = 'subdivision/are/are_form.html'


class AreCreate(LoginRequiredMixin, CreateView):
    model = Are
    fields = ['name', 'forname', 'email', 'telmob', 'adress1', 'adress2', 'town',
              'postalcode', 'tel2', 'phone_hop', 'phone_secretary', 'rpps',
              'coNum', 'secteur']
    template_name = 'subdivision/are/are_create.html'


class AreDelete(LoginRequiredMixin, DeleteView):
    model = Are
    template_name = 'subdivision/are/are_delete.html'
    success_url = reverse_lazy('are_list')


####### CRUD IADE ################ CRUD IADE ################ CRUD IADE #########
'''
class IadeList(LoginRequiredMixin, ListView):
    model = Iade
    template_name = 'subdivision/iade/iade_list.html'


class IadeDetail(LoginRequiredMixin, DetailView):
    model = Iade
    template_name = 'subdivision/iade/iade_detail.html'


class IadeUpdate(LoginRequiredMixin, UpdateView):
    model = Iade
    fields = ['name', 'forname', 'email', 'telmob', 'phone_hop', 'statut']
    template_name = 'subdivision/iade/iade_form.html'


class IadeCreate(LoginRequiredMixin, CreateView):
    model = Iade
    fields = ['name', 'forname', 'email', 'telmob', 'phone_hop', 'statut']
    template_name = 'subdivision/iade/iade_create.html'


class IadeDelete(LoginRequiredMixin, DeleteView):
    model = Iade
    template_name = 'subdivision/iade/iade_delete.html'
    success_url = reverse_lazy('iade_list')'''