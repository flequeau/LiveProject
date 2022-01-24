from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator
from django.shortcuts import render

from .models import Vacation


# Create your views here.
@login_required()
def vacview(request):
    vac_list = Vacation.objects.all().order_by('-start')
    paginator = Paginator(vac_list, 5)
    page = request.GET.get('page')
    vacations = paginator.get_page(page)
    return render(request, 'vacations/vac.html', {'vacations': vacations})
