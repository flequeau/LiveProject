import json
from datetime import datetime
from datetime import timedelta

from django import http
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.core.mail import send_mail
from django.core.paginator import Paginator
from django.http import JsonResponse
from django.shortcuts import render, redirect, get_object_or_404
from django.template.loader import render_to_string
from django.views.generic import ListView, DetailView
from django.views.generic.edit import UpdateView

from LiveProject import settings
from subdivision.models import Event
from .forms import EventFormRepart, RepartLineForm, CsLineForm
from .models import RepartEvent, RepartLine, Room, RepartCs, DeskRoom


def export(request, pk):
    repart = get_object_or_404(RepartEvent, pk=pk)
    matin_lines = RepartLine.objects.all().filter(repart=repart, period='Matin').order_by('room__sortnum')
    apm_lines = RepartLine.objects.all().filter(repart=repart, period='Apm').order_by('room__sortnum')
    matin_cs = RepartCs.objects.all().filter(repart=repart, period='Matin')
    apm_cs = RepartCs.objects.all().filter(repart=repart, period='Apm')
    remplas = Event.objects.all().filter(start=repart.start)
    return render(request, 'repart/export.html', {'matin_lines': matin_lines,
                                                  'apm_lines': apm_lines,
                                                  'repart': repart,
                                                  'matin_cs': matin_cs,
                                                  'apm_cs': apm_cs,
                                                  'remplas': remplas
                                                  })


def emailing(request, pk):
    sender = settings.EMAIL_HOST_USER
    mes_deb = "Bonsoir,\n\n"
    mes_fin = "\n\nA demain"
    repart = get_object_or_404(RepartEvent, pk=pk)
    lines = RepartLine.objects.all().filter(repart=pk, period='Matin')
    subject = "Affectation matin du " + repart.start.strftime('%d-%m-%Y')
    for line in lines:
        test = line.operator_id
        if test is not None:
            salle = line.room.number
            debut = line.start_time
            chir = line.operator.name
            are = line.are.name
            message = F"{mes_deb}Salle: {salle} - Op??rateur: Dr {chir} - D??but: {debut}.{mes_fin}"
            send_mail(subject, message, sender, [line.are.email], fail_silently=True)  # Envoi ?? l'ARE
            if line.iade:
                iade = line.iade
                message = F"{mes_deb}Salle: {salle} - Op??rateur: {chir} - D??but: {debut} - Bin??me IADE: {iade}.{mes_fin}"
                send_mail(subject, message, sender, [line.are.email], fail_silently=True)  # Envoi ?? l'ARE
                message = F"{mes_deb}Salle: {salle} - Op??rateur: {chir} - D??but: {debut} - Anesth??siste: {are}.{mes_fin}"
                send_mail(subject, message, sender, [line.iade.email], fail_silently=True)  # Envoi ?? l'IADE
            if line.interne:
                interne = line.interne.forname
                message = F"{mes_deb}Salle {salle} - Op??rateur {chir} - D??but {debut} - Interne: {interne}.{mes_fin}"  # Envoi ?? l'ARE
                send_mail(subject, message, sender, [line.are.email], fail_silently=True)
                message = F"{mes_deb}Salle {salle} - Op??rateur {chir} - D??but {debut} - Anesth??siste: {are}.{mes_fin}"  # Envoi ?? l'Interne
                send_mail(subject, message, sender, [line.interne.email], fail_silently=True)
    return redirect(export, pk)


@login_required()
def repartview(request):
    repart_list = RepartEvent.objects.all().order_by('-start')
    paginator = Paginator(repart_list, 5)
    page = request.GET.get('page')
    reparts = paginator.get_page(page)
    return render(request, 'repart/repart.html', {'reparts': reparts})


@login_required()
def repartadd(request):
    if request.method == 'POST':
        form = EventFormRepart(request.POST)
        if form.is_valid():
            form.save()
            return redirect('repartadd')
    else:
        form = EventFormRepart(initial={'start_time': '00:00:00', 'end_time': '00:00:00'})
    return render(request, 'repart/repevent.html', {'form': form})


class RepartList(LoginRequiredMixin, ListView):
    model = RepartEvent
    template_name = 'repart/repevent_list.html'
    pass


@login_required
def events_json(request):
    today = datetime.now()
    anneeprev = today - timedelta(weeks=52)
    anneepost = today + timedelta(weeks=52)
    events = RepartEvent.objects.filter(start__range=(anneeprev, anneepost))
    event_list = []
    for event in events:
        event_start = event.start
        event_end = event.end
        event_list.append({
            'id': event.id,
            'start': event_start.strftime('%Y-%m-%d'),
            'end': event_end.strftime('%Y-%m-%d'),
            'title': event.title,
        })
    if len(event_list) == 0:
        raise http.Http404
    else:
        return http.HttpResponse(json.dumps(event_list),
                                 content_type='application/json')


@login_required()
def repartcreate(request, start, end):
    start_event = start[4:8] + '-' + start[2:4] + '-' + start[:2]
    start_event = datetime.strptime(start_event, '%Y-%m-%d')
    end_event = end[4:8] + '-' + end[2:4] + '-' + end[:2]
    end_event = datetime.strptime(end_event, '%Y-%m-%d')
    start = start[:2] + '/' + start[2:4] + '/' + start[4:8]
    if RepartEvent.objects.filter(start=start_event):
        message = 'Une r??partition existe d??j?? pour cette date.'
        return render(request, 'repart/repart.html', {'message': message})
    else:
        pass
    if request.method == 'POST':
        form = EventFormRepart(request.POST)
        if form.is_valid():
            instance = form.save(commit=False)
            instance.title = '{} - {}'.format(instance.duty.name, instance.sspi.name)
            instance.start = start_event
            instance.end = end_event
            instance.duty = instance.duty
            instance.sspi = instance.sspi
            instance.save()
            return redirect('repart')
    else:
        form = EventFormRepart(initial={'start': start})
    return render(request, 'repart/repevent.html', {'form': form})


class RepartUpdate(LoginRequiredMixin, UpdateView):
    model = RepartEvent
    fields = ['start', 'duty', 'sspi', 'title', 'description']
    template_name = 'repart/repevent_update.html'


class RepartDetail(LoginRequiredMixin, DetailView):
    model = RepartEvent
    template_name = 'repart/repevent_detail.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['linerepart_list_matin'] = RepartLine.objects.filter(repart=self.object, period='Matin')
        context['linerepart_list_apm'] = RepartLine.objects.filter(repart=self.object, period='Apm')
        context['csrepart_list_matin'] = RepartCs.objects.filter(repart=self.object, period='Matin')
        context['csrepart_list_apm'] = RepartCs.objects.filter(repart=self.object, period='Apm')
        context['form'] = CsLineForm()
        return context


@login_required()
def LineRepartCreate(request, pk):
    repart = RepartEvent.objects.get(pk=pk)
    rooms = Room.objects.all()
    deskrooms = DeskRoom.objects.all()
    a = RepartLine.objects.filter(repart=repart).count()
    for room in rooms:
        RepartLine.objects.get_or_create(repart=repart, room=room, period='Matin', start_time_id=5)
        RepartLine.objects.get_or_create(repart=repart, room=room, period='Apm')
    for desk in deskrooms:
        RepartCs.objects.get_or_create(repart=repart, deskroom=desk, period='Matin')
        RepartCs.objects.get_or_create(repart=repart, deskroom=desk, period='Apm')
    csreparts = RepartCs.objects.all()
    csrepart_list_matin = csreparts.filter(repart=repart, period='Matin')
    csrepart_list_apm = csreparts.filter(repart=repart, period='Apm')
    linereparts = RepartLine.objects.all()
    linerepart_list_matin = linereparts.filter(repart_id=pk, period__contains='Matin')
    linerepart_list_apm = linereparts.filter(repart_id=pk, period__contains='Apm')
    return render(request, 'repart/repevent_detail.html', {'linerepart_list_matin': linerepart_list_matin,
                                                           'linerepart_list_apm': linerepart_list_apm,
                                                           'csrepart_list_matin': csrepart_list_matin,
                                                           'csrepart_list_apm': csrepart_list_apm,
                                                           'object': repart})


# Modal CRUD Repart ########################################################################


def save_repart_form(request, form, template_name):
    data = dict()
    if request.method == 'POST':
        if form.is_valid():
            instance = form.save(commit=False)
            instance.title = '{} - {}'.format(instance.duty.name, instance.sspi.name)
            instance.save()
            data['form_is_valid'] = True
            reparts = RepartEvent.objects.all()
            data['html_repart_list'] = render_to_string('repart/partial_repart_list.html', {'reparts': reparts})
        else:
            data['form_is_valid'] = False
    context = {'form': form}
    data['html_form'] = render_to_string(template_name, context, request=request)
    return JsonResponse(data)


@login_required()
def repartupdate(request, pk):
    repart = get_object_or_404(RepartEvent, pk=pk)
    if request.method == 'POST':
        form = EventFormRepart(request.POST, instance=repart)
    else:
        form = EventFormRepart(instance=repart)
    return save_repart_form(request, form, 'repart/partial_repart_update.html')


@login_required()
def repartdelete(request, pk):
    repart = get_object_or_404(RepartEvent, pk=pk)
    data = dict()
    if request.method == 'POST':
        repart.delete()
        data['form_is_valid'] = True
        reparts = RepartEvent.objects.all()
        data['html_repart_list'] = render_to_string('repart/partial_repart_list.html', {
            'reparts': reparts
        })
    else:
        context = {'repart': repart}
        data['html_form'] = render_to_string('repart/partial_repart_delete.html', context, request=request)
    return JsonResponse(data)


# Modal CRUD Line Matin ##############################################################################


def save_line_form(request, form, template_name, repart):
    data = dict()
    if request.method == 'POST':
        if form.is_valid():
            form.save()
            data['form_is_valid'] = True
            linerepart_list_matin = RepartLine.objects.all().filter(repart=repart, period="Matin")
            data['html_repart_list'] = render_to_string('line/partial_line_matin_list.html',
                                                        {'linerepart_list_matin': linerepart_list_matin})
        else:
            data['form_is_valid'] = False
    context = {'form': form}
    data['html_form'] = render_to_string(template_name, context, request=request)
    return JsonResponse(data)


@login_required()
def lineupdate(request, pk):
    line = get_object_or_404(RepartLine, pk=pk)
    repart = get_object_or_404(RepartEvent, pk=line.repart.pk)
    if request.method == 'POST':
        form = RepartLineForm(request.POST, instance=line)
    else:
        form = RepartLineForm(instance=line)
    return save_line_form(request, form, 'line/partial_line_update.html', repart)


# Modal CRUD Apr??s-midi ################################################################################


def save_line_apm_form(request, form, template_name, repart):
    data = dict()
    if request.method == 'POST':
        if form.is_valid():
            form.save()
            data['form_is_valid'] = True
            linerepart_list_apm = RepartLine.objects.all().filter(repart=repart, period="Apm")
            data['html_repart_list'] = render_to_string('line/partial_line_apm_list.html',
                                                        {'linerepart_list_apm': linerepart_list_apm})
        else:
            data['form_is_valid'] = False
    context = {'form': form}
    data['html_form'] = render_to_string(template_name, context, request=request)
    return JsonResponse(data)


@login_required()
def lineapmupdate(request, pk):
    line = get_object_or_404(RepartLine, pk=pk)
    repart = get_object_or_404(RepartEvent, pk=line.repart.pk)
    if request.method == 'POST':
        form = RepartLineForm(request.POST, instance=line)
    else:
        form = RepartLineForm(instance=line)
    return save_line_apm_form(request, form, 'line/partial_line_apm_update.html', repart)


# Modal CRUD Cs MATIN ################################################################################

def save_cs_matin_form(request, form, template_name, repart):
    data = dict()
    if request.method == 'POST':
        if form.is_valid():
            form.save()
            data['form_is_valid'] = True
            csrepart_list_matin = RepartCs.objects.all().filter(repart=repart, period="Matin")
            data['html_cs_list'] = render_to_string('cs/partial_cs_matin_list.html',
                                                    {'csrepart_list_matin': csrepart_list_matin})
        else:
            data['form_is_valid'] = False
    context = {'form': form}
    data['html_form'] = render_to_string(template_name, context, request=request)
    return JsonResponse(data)


@login_required()
def csmatinupdate(request, pk):
    cs = get_object_or_404(RepartCs, pk=pk)
    repart = get_object_or_404(RepartEvent, pk=cs.repart.pk)
    if request.method == 'POST':
        form = CsLineForm(request.POST, instance=cs)
    else:
        form = CsLineForm(instance=cs)
    return save_cs_matin_form(request, form, 'cs/partial_cs_update.html', repart)


# Modal CRUD Cs APM ################################################################################

def save_cs_apm_form(request, form, template_name, repart):
    data = dict()
    if request.method == 'POST':
        if form.is_valid():
            form.save()
            data['form_is_valid'] = True
            csrepart_list_apm = RepartCs.objects.all().filter(repart=repart, period="Apm")
            data['html_cs_list'] = render_to_string('cs/partial_cs_apm_list.html',
                                                    {'csrepart_list_apm': csrepart_list_apm})
        else:
            data['form_is_valid'] = False
    context = {'form': form}
    data['html_form'] = render_to_string(template_name, context, request=request)
    return JsonResponse(data)


@login_required()
def csapmupdate(request, pk):
    cs = get_object_or_404(RepartCs, pk=pk)
    repart = get_object_or_404(RepartEvent, pk=cs.repart.pk)
    if request.method == 'POST':
        form = CsLineForm(request.POST, instance=cs)
    else:
        form = CsLineForm(instance=cs)
    return save_cs_apm_form(request, form, 'cs/partial_cs_apm_update.html', repart)
