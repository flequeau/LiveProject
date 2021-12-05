import math
from django.shortcuts import render
from .forms import BloodSaveForm


def blood(request):
    """
    Calcul du volume de réserve
    :param request:
    :return:
    """
    conclusion = ''
    manque = ''
    vol_res = None
    blood_save = {'CS': 150, 'EPO2': 0.04, 'EPO3': 0.06, 'CG': 150}
    form = BloodSaveForm(request.POST or None)
    if request.method == 'POST':
        if form.is_valid():
            response = form.cleaned_data

            # Calcul du volume de réserve actuel
            vol_res = math.floor((int(response['gender']) * response['weight']) * (
                    response['hemacrit_init'] - float(response['hemacrit_final'])))
            vol_res_epo2 = math.floor((int(response['gender']) * response['weight']) * (
                    response['hemacrit_init'] - float(response['hemacrit_final']) + 0.04))
            vol_res_epo3 = math.floor((int(response['gender']) * response['weight']) * (
                    response['hemacrit_init'] - float(response['hemacrit_final']) + 0.06))
            manque = int(response['blood_loss']) - vol_res
            if vol_res <= 0:
                nbre_cg = math.floor(int(response['blood_loss']) / 150)
                conclusion = "Prévoyez {} culots globulaires".format(nbre_cg)
            elif manque <= 0:
                conclusion = "Pas de problème"
            elif manque < 150:
                conclusion = 'Indication de récupération sanguine per-opératoire'
            elif int(response['blood_loss']) - vol_res_epo2 <= 0:
                conclusion = "Indication d'érythropoïne pendant 2 semaines (Nouveau volume de réserve {} ml)".format(
                    vol_res_epo2)
            elif int(response['blood_loss']) - vol_res_epo3 <= 0:
                conclusion = "Indication d'érythropoïne pendant 3 semaines (Nouveau volume de réserve {} ml)".format(
                    vol_res_epo3)
            elif int(response['blood_loss']) - vol_res_epo3 <= 150:
                conclusion = "Indication d'érythropoïne pendant 3 semaines et probablement 1 culot globulaire"
            else:
                nbre_cg = math.floor((int(response['blood_loss']) - vol_res_epo3) / 150)
                conclusion = "3 semaines d'EPO et {} CG nécessaire(s)".format(nbre_cg)

        return render(request, 'calculs/bloodsave.html',
                      {'form': form, 'volume': vol_res, 'conclusion': conclusion, 'manque': manque})
    else:
        form = BloodSaveForm(initial={'weight': 60, 'hemacrit_init': 0.30})

    return render(request, 'calculs/bloodsave.html', {'form': form
                                                       })
