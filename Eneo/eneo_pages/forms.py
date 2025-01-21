from django import forms
from .models import *
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm

# Create your forms here.
#()
class CustomRegistrationForm(UserCreationForm):
    first_name = forms.CharField(widget=forms.TextInput(attrs={
        'placeholder': 'Nom',
        'class': 'form-control'
    }))
    last_name = forms.CharField(widget=forms.TextInput(attrs={
        'placeholder': 'Prénom',
        'class': 'form-control'
    }))
    email = forms.EmailField(widget=forms.EmailInput(attrs={
        'placeholder': 'Adresse mail',
        'class': 'form-control mb-3'
    }))
    username = forms.CharField(widget=forms.TextInput(attrs={
        'placeholder': 'Nom utilisateur',
        'class': 'form-control mb-3'
    }))
    section = forms.ChoiceField(choices=User.Section.choices, widget=forms.Select(attrs={
        'class': 'form-control mb-3'
    }))
    password1 = forms.CharField(widget=forms.PasswordInput(attrs={
        'placeholder': 'Mot de passe',
        'class': 'form-control mb-3'
    }))
    password2 = forms.CharField(widget=forms.PasswordInput(attrs={
        'placeholder': 'Confirmer mot de passe',
        'class': 'form-control mb-3'
    }))

    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'email', 'username', 'section', 'password1', 'password2'] 

class CustomLoginForm(AuthenticationForm):
    username = forms.CharField(widget=forms.TextInput(attrs={
        'placeholder': 'Nom utilisateur',
        'class': 'form-control mb-3'
    }))
    password = forms.CharField(widget=forms.PasswordInput(attrs={
        'placeholder': 'Mot de passe',
        'class': 'form-control mb-3'
    }))

class EquipementForm(forms.ModelForm):
    class Meta:
        model = Equipement
        fields = ['centrale','nom','type_equipement','numero_serie','modèle','marque','puissance','fréquence','date_installation','fonction','emplacement_couplage','regleur_en_chargeur','mode_de_fonctionnement','technique_de_coupure','pouvoir_de_coupure','pression_gaz_nombre_de_pôle','courant_nominal_en_service_continu','numero_service','tension_assigne','pouvoir_de_coupure_nominal_court_circuit','pouvoir_de_fermeture_nominal_court_circuit']
        labels = {'centrale':'Centrale','nom':'Nom','type_equipement':'Type equipement','numero_serie':'Numero serie','modèle':'Modèle','marque':'Marque','puissance':'Puissance','fréquence':'Fréquence','date_installation':'Date installation','fonction':'Fonction','emplacement_couplage':'Emplacement couplage','regleur_en_chargeur':'Regleur en chargeur','mode_de_fonctionnement':'Mode de fonctionnement','technique_de_coupure':'Technique de coupure','pouvoir_de_coupure':'Pouvoir de coupure','pression_gaz_nombre_de_pôle':'Pression gaz nombre de pôle','courant_nominal_en_service_continu':'Courant nominal en service continu','numero_service':'Numero service','tension_assigne':'Tension assigne','pouvoir_de_coupure_nominal_court_circuit':'Pouvoir de coupure nominal court circuit','pouvoir_de_fermeture_nominal_court_circuit':'Pouvoir de fermeture nominal court circuit'}
        widgets = {'centrale': forms.Select(attrs={'class':'form-control'}),
                   'nom': forms.TextInput(attrs={'class':'form-control'}),
                   'type_equipement': forms.Select(attrs={'class':'form-control'}),
                   'numero_serie': forms.TextInput(attrs={'class':'form-control'}),
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


class InterventionUpdateForm(forms.ModelForm):
    class Meta:
        model = Intervention
        fields = ['equipement','type_intervention','date_intervention','date_defaillance','interval_intervention','description','action_correctives','causes_profondes','tache_maintenance','responsable','status','sécurité','coût','coût_materiel','coût_main_oeuvre']
        labels = {'equipement':'Equipement','type_intervention':'Type intervention','date_intervention':'Date intervention','date_defaillance':'Date defaillance','interval_intervention':'Interval intervention','description':'Description','action_correctives':'Action Correctives','causes_profondes':'Causes Profondes','tache_maintenance':'Tache maintenance','responsable':'Responsable','status':'Status','sécurité':'Sécurité','coût_materiel':'Coût Materiel','coût_main_oeuvre':'Coût Main_oeuvre','coût':'Coût Total'}
        widgets = {'equipement': forms.Select(attrs={'class':'form-control'}),
                   'type_intervention': forms.Select(attrs={'class':'form-control'}),
                   'date_intervention': forms.DateInput(attrs={'class':'form-control', 'type':'date'}),
                   'date_defaillance': forms.DateInput(attrs={'class':'form-control', 'type':'date'}),
                   'interval_intervention': forms.TextInput(attrs={'class':'form-control'}),
                   'description': forms.Textarea(attrs={'class':'form-control'}),
                   'action_correctives': forms.Textarea(attrs={'class':'form-control'}),
                   'causes_profondes': forms.Textarea(attrs={'class':'form-control'}),
                   'tache_maintenance': forms.Textarea(attrs={'class':'form-control'}),
                   'responsable': forms.TextInput(attrs={'class':'form-control'}),
                   'status': forms.Select(attrs={'class':'form-control'}),
                   'sécurité': forms.Textarea(attrs={'class':'form-control'}),
                   'coût_materiel': forms.TextInput(attrs={'class':'form-control'}),
                   'coût_main_oeuvre': forms.TextInput(attrs={'class':'form-control'}),
                   'coût': forms.TextInput(attrs={'class':'form-control'}),
                    }
        
class InterventionForm(forms.ModelForm):
    class Meta:
        model = Intervention
        fields = ['equipement','type_intervention','date_intervention','date_defaillance','interval_intervention','description','causes_profondes','responsable','status']
        labels = {'equipement':'Equipement','type_intervention':'Type intervention','date_intervention':'Date intervention','date_defaillance':'Date defaillance','interval_intervention':'Interval intervention','description':'Description','causes_profondes':'Causes Profondes','responsable':'Responsable','status':'Status'}
        widgets = {'equipement': forms.Select(attrs={'class':'form-control'}),
                   'type_intervention': forms.Select(attrs={'class':'form-control', 'id':'type_intervention'}),
                   'date_intervention': forms.DateInput(attrs={'class':'form-control', 'type':'date'}),
                   'date_defaillance': forms.DateInput(attrs={'class':'form-control', 'type':'date'}),
                   'interval_intervention': forms.TextInput(attrs={'class':'form-control', 'id':'interval_intervention'}),
                   'description': forms.Textarea(attrs={'class':'form-control'}),
                   'causes_profondes': forms.Textarea(attrs={'class':'form-control'}),
                   'responsable': forms.TextInput(attrs={'class':'form-control'}),
                   'status': forms.Select(attrs={'class':'form-control'})
                    }
        

class PieceForm(forms.ModelForm):
    class Meta:
        model = Pièce
        fields = ['nom','description','photo','fournisseur','quantité_disponible','prix_unitaire']
        labels = {'nom':'Nom','description':'Description','photo':'Photo','fournisseur':'Fournisseur','quantité_disponible':'Quantité disponible','prix_unitaire':'Prix unitaire'}
        widgets = {'nom': forms.TextInput(attrs={'class':'form-control'}),
                   'description': forms.Textarea(attrs={'class':'form-control'}),
                   'photo': forms.ClearableFileInput(attrs={'class': 'form-control', 'accept': 'image/*'}),
                   'fournisseur': forms.TextInput(attrs={'class':'form-control'}),
                   'quantité_disponible': forms.NumberInput(attrs={'class':'form-control'}),
                   'prix_unitaire': forms.TextInput(attrs={'class':'form-control'}),
                    }

class UtiliserPieceForm(forms.ModelForm):
    class Meta:
        model = Utiliser
        fields = ['piece', 'quantite_prise']
        widgets = {
            'piece': forms.Select(attrs={'class':'form-control'}),
            'quantite_prise': forms.NumberInput(attrs={'class':'form-control'}),
        } 

class DossierForm(forms.ModelForm):
    class Meta:
        model = Dossier
        fields = ['nom','description','fichier']
        labels = {'nom':'Nom','description':'Description','fichier':'Fichier'}
        widgets = {'nom': forms.TextInput(attrs={'class':'form-control'}),
                   'description': forms.Textarea(attrs={'class':'form-control'}),
                   'fichier': forms.ClearableFileInput(attrs={'class': 'form-control', 'accept': 'file/*'}),
                }   