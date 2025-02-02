from django import forms
from .models import *
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django_select2 import forms as s2forms
from dal import autocomplete

class EquipementWidget(s2forms.ModelSelect2Widget):
    search_fields = [
        "nom__icontains",
        "numero_serie__icontains",
    ]

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

class UserProfileUpdateForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ['username', 'email', 'first_name', 'last_name', 'section']
        labels = {
            'username': 'Nom utilisateur',
            'email': 'Adresse mail',
            'first_name': 'Nom',
            'last_name': 'Prénom',
            'section': 'Section',
        }
        widgets = {
            'username': forms.TextInput(attrs={'class': 'form-control'}),
            'email': forms.EmailInput(attrs={'class': 'form-control'}),
            'first_name': forms.TextInput(attrs={'class': 'form-control'}),
            'last_name': forms.TextInput(attrs={'class': 'form-control'}),
            'section': forms.Select(attrs={'class': 'form-control'}),
        }

class EquipementForm(forms.ModelForm):
    class Meta:
        model = Equipement
        fields = '__all__'  # Utiliser tous les champs du modèle
        
    def __init__(self, *args, **kwargs):
        user = kwargs.pop('user', None)
        super(EquipementForm, self).__init__(*args, **kwargs)
        
        # Champs communs
        common_fields = ['centrale', 'nom', 'type_equipement', 'numero_serie', 'modèle', 'marque', 'puissance', 'fréquence', 'date_installation', 'etat_equipement']
        
        # Champs spécifiques aux transformateurs
        transformer_fields = ['fonction', 'emplacement_couplage', 'regleur_en_chargeur', 'mode_de_fonctionnement', 'niveau_tension']
        
        # Champs spécifiques aux disjoncteurs
        disjoncteur_fields = ['technique_de_coupure', 'pouvoir_de_coupure', 'pression_gaz_nombre_de_pôle', 'courant_nominal_en_service_continu', 'numero_service', 'tension_assigne', 'pouvoir_de_coupure_nominal_court_circuit', 'pouvoir_de_fermeture_nominal_court_circuit']

        if user and user.section == 'TRANSFORMATEUR':
            self.fields['type_equipement'].initial = 'Transformateur'
            self.fields['type_equipement'].widget.attrs['disabled'] = True
            # Garder seulement les champs communs et spécifiques aux transformateurs
            fields_to_remove = set(self.fields.keys()) - set(common_fields + transformer_fields)
            for field in fields_to_remove:
                del self.fields[field]
        elif user and user.section == 'DISJONCTEUR':
            self.fields['type_equipement'].initial = 'Disjoncteur'
            self.fields['type_equipement'].widget.attrs['disable'] = True
            # Garder seulement les champs communs et spécifiques aux disjoncteurs
            fields_to_remove = set(self.fields.keys()) - set(common_fields + disjoncteur_fields)
            for field in fields_to_remove:
                del self.fields[field]
        else:
            # Pour les autres utilisateurs, afficher seulement les champs communs
            fields_to_remove = set(self.fields.keys()) - set(common_fields + transformer_fields + disjoncteur_fields)
            for field in fields_to_remove:
                del self.fields[field]
        
        # Appliquer la classe form-control à tous les champs
        for field_name, field in self.fields.items():
            field.widget.attrs.update({'class': 'form-control'})
  
class InterventionForm(forms.ModelForm):
    class Meta:
        model = Intervention
        fields = ['equipement', 'type_intervention', 'date_intervention', 'date_fin_intervention', 'date_defaillance', 'description', 'causes_profondes', 'action_correctives', 'tache_maintenance', 'status', 'responsable', 'sécurité', 'liste_piece_confirmee','coût_materiel', 'coût_main_oeuvre', 'coût']
        labels = {
            'equipement': 'Equipement',
            'type_intervention': 'Type intervention',
            'date_intervention': 'Date debut intervention',
            'date_fin_intervention': 'Date fin intervention',
            'date_defaillance': 'Date defaillance',
            'status': 'Status',
            'responsable': 'Responsable',
            'description': 'Description',
            'causes_profondes': 'Causes Profondes',
            'action_correctives': 'Action Correctives',
            'tache_maintenance': 'Tache maintenance',
            'sécurité': 'Sécurité',
            'liste_piece_confirmee': 'Liste de pièces',
            'coût_materiel': 'Coût Materiel',
            'coût_main_oeuvre': 'Coût Main_oeuvre',
            'coût': 'Coût Total'
        }
        widgets = {
            'equipement': forms.Select(attrs={'class': 'form-control', 'id': 'id_equipement_inter'}),
            'type_intervention': forms.Select(attrs={'class': 'form-control id_type_intervention', 'id': 'id_type_intervention'}),
            'date_intervention': forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}),
            'date_fin_intervention': forms.DateInput(attrs={'class':'form-control', 'type':'date'}),
            'date_defaillance': forms.DateInput(attrs={'class': 'form-control corrective-field', 'type': 'date'}),
            'description': forms.Textarea(attrs={'class': 'form-control preventive-field'}),
            'causes_profondes': forms.Textarea(attrs={'class': 'form-control corrective-field'}),
            'action_correctives': forms.Textarea(attrs={'class': 'form-control corrective-field'}),
            'tache_maintenance': forms.Textarea(attrs={'class': 'form-control corrective-field'}),
            'responsable': forms.TextInput(attrs={'class': 'form-control'}),
            'status': forms.Select(attrs={'class': 'form-control'}),
            'sécurité': forms.Textarea(attrs={'class': 'form-control'}),
            'coût_materiel': forms.TextInput(attrs={'class': 'form-control id_coût_materiel', 'id': 'id_coût_materiel'}),
            'coût_main_oeuvre': forms.TextInput(attrs={'class': 'form-control', 'id': 'id_coût_main_oeuvre'}),
            'coût': forms.TextInput(attrs={'class': 'form-control', 'id': 'id_coût_total'}),
        }

    def __init__(self, *args, **kwargs):
        user = kwargs.pop('user', None)
        super().__init__(*args, **kwargs)

        if user:
        # Filtrer les listes de pièces confirmées pour l'utilisateur actuel
            self.fields['liste_piece_confirmee'] = forms.ModelChoiceField(
                queryset=ListePieceConfirmee.objects.filter(utilisateur=user),
                required=False,
                widget=forms.Select(attrs={'class': 'form-control', 'id': 'id_liste_piece_confirmee'}),
                label="Liste de pièces confirmées"
            )

class PieceForm(forms.ModelForm):
    class Meta:
        model = Pièce
        fields = ['nom','description','photo','fournisseur','quantité_initial','prix_unitaire']
        labels = {'nom':'Nom',
                  'description':'Description',
                  'photo':'Photo',
                  'fournisseur':'Fournisseur',
                  'quantité_initial':'Quantité initiale',
                  'prix_unitaire':'Prix unitaire'
                }
        widgets = {'nom': forms.TextInput(attrs={'class':'form-control'}),
                   'description': forms.Textarea(attrs={'class':'form-control'}),
                   'photo': forms.ClearableFileInput(attrs={'class': 'form-control', 'accept': 'image/*'}),
                   'fournisseur': forms.TextInput(attrs={'class':'form-control'}),
                   'quantité_initial': forms.NumberInput(attrs={'class':'form-control'}),
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
        labels = {'nom':'Nom','fichier':'Fichier','description':'Description'}
        widgets = {'nom': forms.TextInput(attrs={'class':'form-control'}),
                   'description': forms.Textarea(attrs={'class':'form-control'}),
                   'fichier': forms.ClearableFileInput(attrs={'class': 'form-control', 'accept': 'file/*'}),
                }   
        
class PlanificationForm(forms.ModelForm):
    class Meta:
        model = Planification
        fields = ['intervention','equipement', 'frequence', 'heure_homme_requise', 'liste_outillage']
        labels = {'intervention':'Intervention','equipement':'Equipement','frequence':'Fréquence', 'heure_homme_requise':'Heure homme requise', 'liste_outillage':'Liste outillage'}
        widgets = {
            'intervention': forms.Select(attrs={'class':'form-control', 'id':'id_intervention_plan'}),
            'equipement': forms.Select(attrs={'class':'form-control', 'id':'id_equipement_plan'}),
            'frequence': forms.Select(attrs={'class':'form-control'}),
            'heure_homme_requise': forms.NumberInput(attrs={'class':'form-control'}),
            'liste_outillage': forms.Textarea(attrs={'class': 'form-control','rows': 3}),
        }