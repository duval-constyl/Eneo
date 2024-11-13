from datetime import datetime
from django.http import HttpResponseRedirect
from django.shortcuts import redirect, render
from django.urls import reverse, reverse_lazy
from django.views.generic.edit import CreateView,UpdateView,DeleteView
from .models import *
from .forms import *
from tablib import Dataset
from .resources import *
from django.contrib import messages

# Create your views here.
#()
def home(request):
    return render(request, "pages/home.html")

def equipement(request):
    equipement = Equipement.objects.all()
    context = {"liste_equipement" : equipement}
    return render(request, "pages/equipement.html", context)

def detail_equipement(request, id_equip):
    detail_equipement = Equipement.objects.get(id = id_equip)
    context = {"equipement" : detail_equipement}
    return render(request, "equipement/detail.html", context)

class AddEquipement(CreateView):
    model = Equipement
    form_class = EquipementForm
    template_name = "equipement/add.html"
        # Overriding the success_url method to reload the same page after form submission
    def get_success_url(self):
        # Redirects to the same URL after successful submission (i.e., staying on the same page)
        return reverse_lazy('ajouter_equipement')  # Assuming 'ajouter_equipement' is the name of the URL for this view.

    # Override form_valid to clear the form after saving the instance
    def form_valid(self, form):
        response = super().form_valid(form)
        # After the form is successfully saved, clear the form fields
        self.object = form.save()
        form = self.get_form()
        form = EquipementForm()  # Reset the form here
        return response
    
class UpdateEquipement(UpdateView):
    model = Equipement
    form_class = EquipementForm
    template_name = "equipement/update.html"

    def get_success_url(self):
        # Redirects to the same URL after successful submission (i.e., staying on the same page)
        return reverse('detail_equipement', kwargs={'id_equip': self.object.id}) 
    
    def get_object(self, queryset=None):
        return Equipement.objects.get(pk=self.kwargs['pk'])
    
class DeleteEquipement(DeleteView):
    model = Equipement
    template_name = "equipement/detail.html"

    def get_success_url(self):
        # Redirects to the same URL after successful submission (i.e., staying on the same page)
        return reverse('equipement') 
    
    def get_object(self, queryset=None):
        return Equipement.objects.get(pk=self.kwargs['pk'])
    
def importEquipement(request):
    if request.method == 'POST':
        equipe_import = EquipementResources()
        dataset = Dataset()

        # Assurez-vous que le fichier est correctement envoyé
        if 'file' in request.FILES:
            new_equipe = request.FILES['file']
            try:
                # Charger les données à partir du fichier Excel
                imported_data = dataset.load(new_equipe.read(), format='xlsx')

                # Parcourir les données importées et créer des objets Equipement
                for data in imported_data:
                    centrale_nom = data[0]  # Nom de la centrale dans la première colonne du fichier

                    # Trouver ou créer l'instance de Centrale en fonction du nom
                    centrale_instance, created = Centrale.objects.get_or_create(nom=centrale_nom)

                    try:
                        # Création d'un nouvel objet Equipement avec les données importées
                        Equipement.objects.create(
                            centrale=centrale_instance,
                            nom=data[1],
                            type_equipement=data[2],
                            modele=data[3],
                            marque=data[4],
                            puissance=data[5],
                            frequence=data[6],
                            date_installation=datetime.strptime(data[7], '%Y-%m-%d') if data[7] else None,
                            fonction=data[8],
                            emplacement_couplage=data[9],
                            regleur_en_chargeur=data[10],
                            mode_de_fonctionnement=data[11],
                            technique_de_coupure=data[12],
                            pouvoir_de_coupure=data[13],
                            pression_gaz_nombre_de_pole=data[14],
                            courant_nominal_en_service_continu=data[15],
                            numero_service=data[16],
                            tension_assigne=data[17],
                            pouvoir_de_coupure_nominal_court_circuit=data[18],
                            pouvoir_de_fermeture_nominal_court_circuit=data[19]
                        )
                    except Exception as e:
                        # Si une erreur survient lors de la création d'un objet Equipement, l'erreur est capturée
                        messages.error(request, f"Erreur lors de l'importation de l'équipement {data[1]}: {str(e)}")

                # Message de succès après avoir importé toutes les données
                messages.success(request, 'Les équipements ont été importés avec succès.')

            except Exception as e:
                # Si une erreur survient lors du traitement du fichier Excel, l'erreur est capturée
                messages.error(request, f"Erreur lors de l'importation du fichier: {str(e)}")

            # Rediriger l'utilisateur vers la liste des équipements après l'importation
            return redirect('equipement')

    return render(request, 'pages/equipement.html')


def intervention(request):
    intervention = Intervention.objects.all()
    context = {"liste_intervention" : intervention}
    return render(request, "pages/intervention.html", context)

def piece(request):
    piece = Pièce.objects.all()
    context = {"liste_piece" : piece}
    return render(request, "pages/piece.html", context)
