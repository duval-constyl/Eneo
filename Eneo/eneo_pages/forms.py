from django import forms
from .models import *

# Create your forms here.
#()
class EquipementForm(forms.ModelForm):
    class Meta:
        model = Equipement
        fields = ['centrale','nom','type_equipement','modèle','marque','puissance','fréquence','date_installation','fonction','emplacement_couplage','regleur_en_chargeur','mode_de_fonctionnement','technique_de_coupure','pouvoir_de_coupure','pression_gaz_nombre_de_pôle','courant_nominal_en_service_continu','numero_service','tension_assigne','pouvoir_de_coupure_nominal_court_circuit','pouvoir_de_fermeture_nominal_court_circuit']
        labels = {'centrale':'Centrale','nom':'Nom','type_equipement':'Type equipement','modèle':'Modèle','marque':'Marque','puissance':'Puissance','fréquence':'Fréquence','date_installation':'Date installation','fonction':'Fonction','emplacement_couplage':'Emplacement couplage','regleur_en_chargeur':'Regleur en chargeur','mode_de_fonctionnement':'Mode de fonctionnement','technique_de_coupure':'Technique de coupure','pouvoir_de_coupure':'Pouvoir de coupure','pression_gaz_nombre_de_pôle':'Pression gaz nombre de pôle','courant_nominal_en_service_continu':'Courant nominal en service continu','numero_service':'Numero service','tension_assigne':'Tension assigne','pouvoir_de_coupure_nominal_court_circuit':'Pouvoir de coupure nominal court circuit','pouvoir_de_fermeture_nominal_court_circuit':'Pouvoir de fermeture nominal court circuit'}
        widgets = {'centrale': forms.Select(attrs={'class':'form-control'}),
                   'nom': forms.TextInput(attrs={'class':'form-control'}),
                   'type_equipement': forms.Select(attrs={'class':'form-control'}),
                   'modèle': forms.TextInput(attrs={'class':'form-control'}),
                   'marque': forms.TextInput(attrs={'class':'form-control'}),
                   'puissance': forms.TextInput(attrs={'class':'form-control'}),
                   'fréquence': forms.TextInput(attrs={'class':'form-control'}),
                   'date_installation': forms.DateInput(attrs={'class':'form-control'}),
                   'fonction': forms.TextInput(attrs={'class':'form-control'}),
                   'emplacement_couplage': forms.TextInput(attrs={'class':'form-control'}),
                   'regleur_en_chargeur': forms.TextInput(attrs={'class':'form-control'}),
                   'mode_de_fonctionnement': forms.TextInput(attrs={'class':'form-control'}),
                   'technique_de_coupure': forms.TextInput(attrs={'class':'form-control'}),
                   'pouvoir_de_coupure': forms.TextInput(attrs={'class':'form-control'}),
                   'pression_gaz_nombre_de_pôle': forms.TextInput(attrs={'class':'form-control'}),
                   'courant_nominal_en_service_continu': forms.TextInput(attrs={'class':'form-control'}),
                   'numero_service': forms.TextInput(attrs={'class':'form-control'}),
                   'tension_assigne': forms.TextInput(attrs={'class':'form-control'}),
                   'pouvoir_de_coupure_nominal_court_circuit': forms.TextInput(attrs={'class':'form-control'}),
                   'pouvoir_de_fermeture_nominal_court_circuit': forms.TextInput(attrs={'class':'form-control'}),}


class InterventionForm(forms.ModelForm):
    class Meta:
        model = Intervention
        fields = ['equipement','date_intervention','date_defaillance','description','tache_maintenance','responsable','status','coût']
        labels = {'equipement':'Equipement','date_intervention':'Date intervention','date_defaillance':'Date defaillance','description':'Description','tache_maintenance':'Tache maintenance','responsable':'Responsable','status':'Status','coût':'Coût'}
        widgets = {'equipement': forms.Select(attrs={'class':'form-control'}),
                   'date_intervention': forms.DateInput(attrs={'class':'form-control'}),
                   'date_defaillance': forms.DateInput(attrs={'class':'form-control'}),
                   'description': forms.Textarea(attrs={'class':'form-control'}),
                   'tache_maintenance': forms.Textarea(attrs={'class':'form-control'}),
                   'responsable': forms.TextInput(attrs={'class':'form-control'}),
                   'status': forms.Select(attrs={'class':'form-control'}),
                   'coût': forms.TextInput(attrs={'class':'form-control'}),
                    }
        

class PieceForm(forms.ModelForm):
    class Meta:
        model = Pièce
        fields = ['nom','description','photo','quantité_disponible','prix_unitaire']
        labels = {'nom':'Nom','description':'Description','photo':'Photo','quantité_disponible':'Quantité disponible','prix_unitaire':'Prix unitaire'}
        widgets = {'nom': forms.TextInput(attrs={'class':'form-control'}),
                   'description': forms.Textarea(attrs={'class':'form-control'}),
                   'photo' : forms.ImageField(required=False, widget=forms.ClearableFileInput(attrs={'class': 'form-control', 'accept': 'image/*'})),
                   'quantité_disponible': forms.TextInput(attrs={'class':'form-control'}),
                   'prix_unitaire': forms.TextInput(attrs={'class':'form-control'}),
                    }