from django.contrib import admin
from subdivision.models import Calendrier, WebColor, Are, Rpt, HopParam, Event
from repartition.models import Room, RepartEvent, DeskRoom, Iade, Operator, Sector, RepartLine, HourChoice, RepartCs, \
    Interne
from vacations.models import Vacataire, Vacation

admin.site.register(Calendrier)
admin.site.register(WebColor)
admin.site.register(Are)
admin.site.register(Rpt)
admin.site.register(HopParam)
admin.site.register(Event)
admin.site.register(HourChoice)
admin.site.register(Sector)
admin.site.register(Room)
admin.site.register(RepartEvent)
admin.site.register(RepartCs)
admin.site.register(RepartLine)
admin.site.register(DeskRoom)
admin.site.register(Iade)
admin.site.register(Interne)
admin.site.register(Operator)
admin.site.register(Vacataire)
admin.site.register(Vacation)
