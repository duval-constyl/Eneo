from django.shortcuts import render
from .models import *

# Create your views here.
#()
def home(request):
    return render(request, "pages/home.html")

def equipement(request):
    equipement = Equipement.objects.all()
    context = {"liste_equipement" : equipement}
    return render(request, "pages/equipement.html", context)

def intervention(request):
    intervention = Intervention.objects.all()
    context = {"liste_intervention" : intervention}
    return render(request, "pages/intervention.html", context)

def piece(request):
    piece = Pièce.objects.all()
    context = {"liste_piece" : piece}
    return render(request, "pages/piece.html", context)
