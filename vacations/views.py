import json
from datetime import datetime, timedelta

from django import http
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator
from django.shortcuts import render, redirect

from .forms import VacForm
from .models import Vacation


# Create your views here.
@login_required()
def vacview(request):
    vac_list = Vacation.objects.all().order_by('-start')
    paginator = Paginator(vac_list, 5)
    page = request.GET.get('page')
    vacations = paginator.get_page(page)
    return render(request, 'vacations/vac.html', {'vacations': vacations})


@login_required()
def events_json(request):
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


def create(request, start, end):
    start_event = start[4:8] + '-' + start[2:4] + '-' + start[:2]
    start_event = datetime.strptime(start_event, '%Y-%m-%d')
    end_event = end[4:8] + '-' + end[2:4] + '-' + end[:2]
    end_event = datetime.strptime(end_event, '%Y-%m-%d')
    start = start[:2] + '/' + start[2:4] + '/' + start[4:8]
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
            return redirect('vacation')
        else:
            message = 'Le vacataire a déjà un contrat à cette date'
            return render(request, 'vacations/event.html',
                          {'form': form, 'message': message, 'idems': idems})
    else:
        form = VacForm(initial={'start': start_event, 'end': end_event})
        return render(request, 'vacations/event.html', {'form': form, 'idems': idems})
