import json
from datetime import datetime, timedelta, date

from django import http
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator
from django.shortcuts import render, redirect, get_object_or_404

from .forms import VacForm
from .models import Vacation


# Create your views here.
@login_required()
def vacview(request, day=None):
    vac_list = Vacation.objects.all().order_by('-start')
    paginator = Paginator(vac_list, 5)
    page = request.GET.get('page')
    vacations = paginator.get_page(page)
    day = date.today()
    return render(request, 'vacations/vac.html', {'vacations': vacations,
                                                  'day': day})


@login_required()
def vac_events_json(request):
    today = datetime.now()
    anneeprev = today - timedelta(weeks=52)
    anneepost = today + timedelta(weeks=52)
    events = Vacation.objects.filter(start__range=(anneeprev, anneepost))
    event_list = []

    for event in events:
        event_list.append({
            'id': event.id,
            'start': '{}T{}'.format(event.start.strftime('%Y-%m-%d'), event.start_time.strftime('%H:%M:%S')),
            'end': '{}T{}'.format(event.start.strftime('%Y-%m-%d'), event.end_time.strftime('%H:%M:%S')),
            'title': event.title,
            'color': event.vacataire.color.colorHex
        })
    if len(event_list) == 0:
        raise http.Http404
    else:
        return http.HttpResponse(json.dumps(event_list),
                                 content_type='application/json')


def vaccreate(request, start, end):
    start_event = start[0:10]
    start_event = datetime.strptime(start_event, '%Y-%m-%d')
    end_event = end[0:10]
    end_event = datetime.strptime(end_event, '%Y-%m-%d')
    if Vacation.objects.filter(start=start_event).exists:
        idems = Vacation.objects.filter(start=start_event)
    else:
        idems = ''
    if request.method == 'POST':
        form = VacForm(request.POST)
        if form.is_valid():
            instance = form.save(commit=False)
            instance.title = instance.vacataire.name + ' ' + instance.vacataire.forname
            instance.calendrier_id = 4
            instance.save()
            day = start_event
            return render(request, 'vacations/vac.html', {'day': day})
        else:
            message = 'Le vacataire a déjà un contrat à cette date'
            return render(request, 'vacations/event.html',
                          {'form': form, 'message': message, 'idems': idems})
    else:
        form = VacForm(initial={'start': start_event, 'end': end_event})
        return render(request, 'vacations/event.html', {'form': form, 'idems': idems})


@login_required()
def vacupdate(request, id):
    event = get_object_or_404(Vacation, pk=id)
    event_idems = Vacation.objects.filter(start=event.start).exclude(pk=id)
    form = VacForm(request.POST or None, instance=event)
    if request.method == 'POST':
        if form.is_valid():
            form.save()
            day = event.start
            return render(request, 'vacations/vac.html', {'day': day})
    else:
        return render(request, 'vacations/event.html', {'form': form,
                                                        'id': id,
                                                        'start': event.start,
                                                        'title': event.title,
                                                        'start_time': event.start_time,
                                                        'end_time': event.end_time,
                                                        'vacataire': event.vacataire,
                                                        'idems': event_idems,
                                                        })


@login_required()
def vacresize(request, id, start, end):
    event = get_object_or_404(Vacation, pk=id)
    start_new = start[0:10]
    end_new = end[0:10]
    start_time_new = start[11:19]
    end_time_new = end[11:19]
    event.start = start_new
    event.end = end_new
    event.start_time = start_time_new
    event.end_time = end_time_new
    event.save()
    event = get_object_or_404(Vacation, pk=id)
    day = event.start
    return render(request, 'vacations/vac.html', {'day': day})


@login_required()
def vacdelete(request, id):
    event = get_object_or_404(Vacation, pk=id)
    day = event.start
    event.delete()
    return render(request, 'vacations/vac.html', {'day': day})