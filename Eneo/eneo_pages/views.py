from datetime import datetime
from itertools import count
import logging
from django.http import HttpResponse, JsonResponse
from django.shortcuts import redirect, render
from django.urls import reverse, reverse_lazy
from django.views.generic.edit import CreateView,UpdateView,DeleteView
from django.contrib.auth.mixins import LoginRequiredMixin
from .models import *
from .forms import *
from .resources import *
from django.contrib import messages
from openpyxl import load_workbook
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.conf import settings
from django.core.mail import EmailMessage
from django.utils import timezone
from django.contrib.auth import login, get_user_model
from django.db.models import Prefetch
from django. shortcuts import render
from .documents import *
from django.db.models import Q
from elasticsearch_dsl import Q as ESQ
from django.db import transaction
from django.shortcuts import get_object_or_404
from django.views.decorators.http import require_POST
from django.views.decorators.csrf import csrf_protect
import json
from datetime import datetime


@login_required
def home(request):    
    User = get_user_model()  # Get the custom user model
    user = request.user  # Get the currently logged-in user

    # Rubrique intervention jour
    # Obtenir la date du jour
    today = timezone.now().date()
    if user.section == 'DISJONCTEUR':
        intervention_date = Intervention.objects.filter(equipement__type_equipement='Disjoncteur', date_intervention=today)
    elif user.section == 'TRANSFORMATEUR':
        intervention_date = Intervention.objects.filter(equipement__type_equipement='Transformateur', date_intervention=today)
    else:
        intervention_date = Intervention.objects.filter(date_intervention=today)

    #Rubrique intervention en panne
    if user.section == 'DISJONCTEUR':
        intervention_status = Intervention.objects.filter(equipement__type_equipement='Disjoncteur', status='En panne')
    elif user.section == 'TRANSFORMATEUR':
        intervention_status = Intervention.objects.filter(equipement__type_equipement='Transformateur', status='En panne')
    else:
        intervention_status = Intervention.objects.filter(status='En panne')

    # Rubrique pièce
    pieces = Pièce.objects.all()  # Récupérer toutes les pièces
    total_pieces = pieces.count()  # Compter le nombre total de pièces
    total_montant = sum((piece.prix_unitaire * piece.quantité_disponible) for piece in pieces)  # Calculer le montant total des pièces Rubrique piece

    # Rubrique équipement
    # Filter equipment based on user section
    if user.section == 'DISJONCTEUR':
        liste_equipement = Equipement.objects.filter(type_equipement='Disjoncteur')
    elif user.section == 'TRANSFORMATEUR':
        liste_equipement = Equipement.objects.filter(type_equipement='Transformateur')
    else:
        liste_equipement = Equipement.objects.all()

    context = {
        "liste_equipement" : liste_equipement,
        "liste_intervention_date" : intervention_date,
        "liste_intervention_status" : intervention_status,
        "total_pieces": total_pieces,
        "total_montant": total_montant,
    }
    return render(request, "pages/home.html", context)

@login_required
def intervention_home(request):
    User = get_user_model()  # Get the custom user model
    user = request.user  # Get the currently logged-in user
     # Obtenir la date du jour
    today = timezone.now().date()
    
    # Filter equipment based on user section
    if user.section == 'DISJONCTEUR':
        intervention_date = Intervention.objects.filter(equipement__type_equipement='Disjoncteur', date_intervention=today)
    elif user.section == 'TRANSFORMATEUR':
        intervention_date = Intervention.objects.filter(equipement__type_equipement='Transformateur', date_intervention=today)
    else:
        intervention_date = Intervention.objects.filter(date_intervention=today)

    context_date = {"liste_intervention_date" : intervention_date}
    return render(request, "pages/home.html", context_date)

# Auth views
def RegisterView(request):
    if request.method == 'POST':
        form = CustomRegistrationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('login')
    else:
        form = CustomRegistrationForm()
    return render(request, 'auth/register.html', {'form':form})

def LoginView(request):
    if request.method == 'POST':
        form = CustomLoginForm(request, request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password') 
            
            user = authenticate(request, username=username, password=password)

            if user is not None:
                login(request, user)
                return redirect('home')
            else:
                form.add_error(None, 'Invalid username or password')
    else:
        form = CustomLoginForm() 

    return render(request, 'auth/login.html', {'form': form})

def LogoutView(request):

    logout(request)

    # redirect to login page after logout
    return redirect('login')

def ForgotPassword(request):
    User = get_user_model()
    if request.method == 'POST':
        email = request.POST.get('email')

        # verify if email exists
        try:
            user = User.objects.get(email=email)

            # create a new reset id
            new_password_reset = PasswordReset(utilisateur=user)
            new_password_reset.save()

            # creat password reset ur;
            password_reset_url = reverse('reset-password', kwargs={'reset_id': new_password_reset.id_modification})

            # email content
            email_body = f'Réinitialisez votre mot de passe en cliquant sur ce lien:\n\n\n{password_reset_url}',

            email_message = EmailMessage(
                'Réinitialisation mot de passe', # email subject
                email_body,
                settings.EMAIL_HOST_USER, # email sender
                [email] # email  receiver 
            )

            email_message.fail_silently = True
            email_message.send()

            return redirect('password-reset-sent')

        except User.DoesNotExist:
            messages.error(request, f"Aucun utilisateur trouvé avec ce mail '{email}'")
            return redirect('forgot-password')
        
    return render(request, 'auth/forgot_password.html')

def PasswordResetSent(request, reset_id):
    if PasswordReset.objects.filter(id_modification=reset_id).exists():
        return render(request, 'auth/password_reset_sent.html')
    else:
        # redirect to forgot password page if code does not exist
        messages.error(request, 'Id de la réinitialisation erroné')
        return redirect('forgot-password')

def ResetPassword(request, reset_id):
    if request.method == 'POST':

        password = request.POST.get('password')
        confirm_password = request.POST.get('confirm_password')

        passwords_have_error = False

        if password != confirm_password:
            passwords_have_error = True
            messages.error(request, 'Mot de passe ne concorde pas')

        if len(password) < 5:
            passwords_have_error = True
            messages.error(request, 'Votre mot de passe doit avoir une longueur minimum de 5 caractere')

        expiration_time = reset_id.created_when + timezone.timedelta(minutes=10)

        if timezone.now() > expiration_time:

            # delete reset id if expired
            reset_id.delete()

            passwords_have_error = True
            messages.error(request, 'Votre lien de réinitialisation est expiré')
        
        # reset password
        if not passwords_have_error:
            user = reset_id.user
            user.set_password(password)
            user.save()
            
            # delete reset id after use
            reset_id.delete()

            # redirect to login
            messages.success(request, 'Mot de passe réinitialisé, connectez vous')
            return redirect('login')

        else:
            # redirect back to password reset page and display errors
            return redirect('reset-password', reset_id=reset_id)
    
    return render(request, 'auth/reset_password.html')



# Modules Equipement
@login_required
def equipement(request):
    context = {}
    q = request.GET.get("q")
    
    User = get_user_model()
    user = request.user

    # Filtrer les équipements en fonction de la section de l'utilisateur
    if user.section == 'DISJONCTEUR':
        base_queryset = Equipement.objects.filter(type_equipement='Disjoncteur')
    elif user.section == 'TRANSFORMATEUR':
        base_queryset = Equipement.objects.filter(type_equipement='Transformateur')
    else:
        base_queryset = Equipement.objects.all()

    if q:
        # Recherche Elasticsearch
        s = EquipementDocument.search().query(
            ESQ("multi_match", 
                query=q, 
                fields=['nom', 'type_equipement', 'numero_serie', 'modèle', 'marque']
            )
        )
        es_results = s.to_queryset()
        
        # Recherche Django ORM
        db_results = base_queryset.filter(
            Q(nom__icontains=q) | 
            Q(type_equipement__icontains=q) | 
            Q(numero_serie__icontains=q) | 
            Q(modèle__icontains=q) | 
            Q(marque__icontains=q)
        )
        
        # Combiner les résultats
        liste_equipement = (es_results & base_queryset) | db_results
    else:
        liste_equipement = base_queryset

    context["liste_equipement"] = liste_equipement.distinct()
    
    return render(request, "pages/equipement/equipement.html", context)

@login_required
def detail_equipement(request, id_equip):
    detail_equipement = Equipement.objects.get(id = id_equip)
    context = {"equipement" : detail_equipement}
    return render(request, "pages/equipement/detail.html", context)

class AddEquipement(LoginRequiredMixin, CreateView):
    model = Equipement
    form_class = EquipementForm
    template_name = "pages/equipement/add.html"
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
    
class UpdateEquipement(LoginRequiredMixin, UpdateView):
    model = Equipement
    form_class = EquipementForm
    template_name = "pages/equipement/update.html"

    def get_success_url(self):
        # Redirects to the same URL after successful submission (i.e., staying on the same page)
        return reverse('detail_equipement', kwargs={'id_equip': self.object.id}) 
    
    def get_object(self, queryset=None):
        return Equipement.objects.get(pk=self.kwargs['pk'])

class DeleteEquipement(LoginRequiredMixin, DeleteView):
    model = Equipement
    template_name = "pages/equipement/detail.html"

    def get_success_url(self):
        # Redirects to the same URL after successful submission (i.e., staying on the same page)
        return reverse('equipement') 
    
    def get_object(self, queryset=None):
        return Equipement.objects.get(pk=self.kwargs['pk'])

logger = logging.getLogger(__name__)

@login_required
@transaction.atomic
def importEquipement(request):
    def map_type_equipement(value):
        valid_types = ["transformateur", "disjoncteur"]
        return value.capitalize() if value.lower() in valid_types else ""


    if request.method == 'POST':
        if 'file' not in request.FILES:
            messages.error(request, "Aucun fichier n'a été uploadé.")
            return render(request, 'pages/equipement/equipement.html')
        
        excel_file = request.FILES['file']
        
        if not excel_file.name.endswith(('.xlsx', '.xls')):
            messages.error(request, 'Mauvais type de fichier. Veuillez uploader un fichier Excel (.xlsx ou .xls).')
            return render(request, 'pages/equipement/equipement.html')
        
        try:
            wb = load_workbook(excel_file, data_only=True)
            ws = wb.active
            equipements_created = 0
            equipements_updated = 0

            for row in ws.iter_rows(min_row=2, values_only=True):
                if not row[0]:
                    continue
                
                logger.info(f"Processing row: {row}")
                
                centrale_nom = row[0]
                centrale_instance, _ = Centrale.objects.get_or_create(nom=centrale_nom)
                
                date_installation = None
                if row[8]:
                    if isinstance(row[8], datetime):
                        date_installation = row[8].date()
                    else:
                        try:
                            date_installation = datetime.strptime(str(row[8]), '%Y-%m-%d').date()
                        except ValueError:
                            logger.warning(f"Format de date invalide pour la ligne: {row}")

                type_equipement = map_type_equipement(row[2])
                logger.info(f"Mapped equipment type: {type_equipement}")

                
                if type_equipement:
                    equipement, created = Equipement.objects.update_or_create(
                        centrale=centrale_instance,
                        nom=row[1],
                        numero_serie=row[3],
                        defaults={
                            'type_equipement': type_equipement,
                            'modèle': row[4] or '',
                            'marque': row[5] or '',
                            'fréquence': float(row[6]) if row[6] else 0,
                            'puissance': float(row[7]) if row[7] else 0,
                            'date_installation': date_installation,
                            'fonction': row[9] or '',
                            'emplacement_couplage': row[10] or '',
                            'regleur_en_chargeur': row[11] or '',
                            'mode_de_fonctionnement': row[12] or '',
                            'technique_de_coupure': row[13] or '',
                            'pouvoir_de_coupure': row[14] or '',
                            'pression_gaz_nombre_de_pôle': row[15] or '',
                            'courant_nominal_en_service_continu': row[16] or '',
                            'numero_service': row[17] or '',
                            'tension_assigne': row[18] or '',
                            'pouvoir_de_coupure_nominal_court_circuit': row[19] or '',
                            'pouvoir_de_fermeture_nominal_court_circuit': row[20] or ''
                        }
                    )

                    if created:
                        logger.info(f"Created equipement: {equipement}")
                        equipements_created += 1
                    else:
                        logger.info(f"Updated equipement: {equipement}")
                        equipements_updated += 1
                else:
                    logger.warning(f"Type d'équipement invalide pour la ligne: {row}")

            logger.info(f"Total equipements created: {equipements_created}")
            logger.info(f"Total equipements updated: {equipements_updated}")
            messages.success(request, f"Importation réussie. {equipements_created} équipements créés, {equipements_updated} équipements mis à jour.")
            return redirect('equipement')
        except Exception as e:
            logger.error(f"Error during import: {str(e)}", exc_info=True)
            messages.error(request, f"Une erreur s'est produite lors de l'importation : {str(e)}")
            return render(request, 'pages/equipement/equipement.html')

    return render(request, 'base/import.html')

# Module Intervention
@login_required
def intervention(request):
    context = {}
    q = request.GET.get("q")

    User = get_user_model()  # Get the custom user model
    user = request.user  # Get the currently logged-in user
    
    # Filter equipment based on user section
    if user.section == 'DISJONCTEUR':
        base_queryset = Intervention.objects.filter(equipement__type_equipement='Disjoncteur')
    elif user.section == 'TRANSFORMATEUR':
        base_queryset = Intervention.objects.filter(equipement__type_equipement='Transformateur')
    else:
        base_queryset = Intervention.objects.all()

    if q:
        # Recherche Elasticsearch
        s = InterventionDocument.search().query(
            ESQ("multi_match", 
                query=q, 
                fields=['type_intervention', 'responsable', 'status', 'description', 'tache_maintenance', 'action_correctives', 'causes_profondes']
            )
        )
        es_results = s.to_queryset()
        
        # Recherche Django ORM
        db_results = base_queryset.filter(
            Q(type_intervention__icontains=q) | 
            Q(responsable__icontains=q) | 
            Q(status__icontains=q) | 
            Q(description__icontains=q) | 
            Q(tache_maintenance__icontains=q) |
            Q(action_correctives__icontains=q) | 
            Q(causes_profondes__icontains=q) 
        )
        
        # Combiner les résultats
        liste_intervention = (es_results & base_queryset) | db_results
    else:
        liste_intervention = base_queryset
    
    context["liste_intervention"] = liste_intervention.distinct()
    return render(request, "pages/intervention/intervention.html", context)

@login_required
def detail_intervention(request, id_intervention):
    detail_intervention = Intervention.objects.get(id = id_intervention)
    context = {"intervention" : detail_intervention}
    return render(request, "pages/intervention/detail.html", context)

class AddIntervention(LoginRequiredMixin, CreateView):
    model = Intervention
    form_class = InterventionForm
    template_name = "pages/intervention/add.html"
        # Overriding the success_url method to reload the same page after form submission
    def get_success_url(self):
        # Redirects to the same URL after successful submission (i.e., staying on the same page)
        return reverse_lazy('intervention')  # Assuming 'ajouter_equipement' is the name of the URL for this view.

    # Override form_valid to clear the form after saving the instance
    def form_valid(self, form):
        response = super().form_valid(form)
        # After the form is successfully saved, clear the form fields
        self.object = form.save()
        form = self.get_form()
        form = InterventionForm()  # Reset the form here
        return response

class UpdateIntervention(LoginRequiredMixin, UpdateView):
    model = Intervention
    form_class = InterventionUpdateForm
    template_name = "pages/intervention/update.html"

    def get_success_url(self):
        return reverse_lazy('intervention')   
    
    def get_object(self, queryset=None):
        return Intervention.objects.get(pk=self.kwargs['pk'])
    
class DeleteIntervention(LoginRequiredMixin, DeleteView):
    model = Intervention
    template_name = "pages/intervention/delete.html"

    def get_success_url(self):
        return reverse_lazy('intervention')  
    
    def get_object(self, queryset=None):
        return Intervention.objects.get(pk=self.kwargs['pk'])


# Module Pièce de réchange
@login_required
def piece(request):
    context = {}
    q = request.GET.get("q")
    base_queryset = Pièce.objects.all()

    if q:
        # Recherche Elasticsearch
        s = PièceDocument.search().query(
            ESQ("multi_match", 
                query=q, 
                fields=['nom', 'description', 'fournisseur']
            )
        )
        es_results = s.to_queryset()
        
        # Recherche Django ORM
        db_results = base_queryset.filter(
            Q(nom__icontains=q) | 
            Q(description__icontains=q) | 
            Q(fournisseur__icontains=q) 
        )
        
        # Combiner les résultats
        liste_piece = (es_results & base_queryset) | db_results
    else:
        liste_piece = base_queryset

    context["liste_piece"] = liste_piece.distinct()
    return render(request, "pages/piece/piece.html", context)

@login_required
def detail_piece(request, id_piece):
    detail_piece = Pièce.objects.get(id = id_piece)
    context = {"piece" : detail_piece}
    return render(request, "pages/piece/detail.html", context)

class AddPiece(LoginRequiredMixin, CreateView):
    model = Pièce
    form_class = PieceForm
    template_name = "pages/piece/add.html"

    def get_success_url(self):
        return reverse_lazy('piece') 

    def form_valid(self, form):
        response = super().form_valid(form)
        self.object = form.save()
        form = self.get_form()
        form = PieceForm()
        return response
 
class UpdatePiece(LoginRequiredMixin, UpdateView):
    model = Pièce
    form_class = PieceForm
    template_name = "pages/piece/update.html"

    def get_success_url(self):
        return HttpResponse(reverse('piece'))
    
    def get_object(self, queryset=None):
        return Pièce.objects.get(pk=self.kwargs['pk'])

class DeletePiece(LoginRequiredMixin, DeleteView):
    model = Pièce
    template_name = "pages/piece/delete.html"

    def get_success_url(self):
        return HttpResponse(reverse('piece'))
    
    def get_object(self, queryset=None):
        return Pièce.objects.get(pk=self.kwargs['pk'])

def view_cart(request):
    cart = request.session.get('cart', {})
    cart_items = [{'id': k, 'nom': v['nom'], 'quantite': v['quantite'], 'prix': v['prix']} for k, v in cart.items()]
    total_price = sum(item['quantite'] * item['prix'] for item in cart_items)
    context = {
        'cart_items': cart_items,
        'total_price': total_price,
    }
    return render(request, 'pages/piece/gestion_pieces.html', context)

def add_to_cart(request, piece_id):
    piece = Pièce.objects.get(id=piece_id)
    cart = request.session.get('cart', {})
    
    if str(piece_id) in cart:
        cart[str(piece_id)]['quantite'] += 1
    else:
        cart[str(piece_id)] = {'quantite': 1, 'nom': piece.nom, 'prix': float(piece.prix_unitaire)}
    
    request.session['cart'] = cart
    total_quantity = sum(item['quantite'] for item in cart.values())
    
    return redirect('piece') 

def get_cart_quantity(request):
    cart = request.session.get('cart', {})
    if not cart:
        return JsonResponse({'quantity': 0})
    total_quantity = sum(item['quantite'] for item in cart.values())
    return JsonResponse({'quantity': total_quantity})


def remove_from_cart(request, piece_id):
    cart = request.session.get('cart', {})
    if str(piece_id) in cart:
        del cart[str(piece_id)]
        request.session['cart'] = cart
    return redirect('piece')

@transaction.atomic
def confirm_cart(request):
    if request.method == 'POST':
        cart = request.session.get('cart', {})
        if cart:
            liste_confirmee = ListePieceConfirmee.objects.create(utilisateur=request.user)
            for piece_id, item in cart.items():
                piece = get_object_or_404(Pièce, id=piece_id)
                PieceConfirmee.objects.create(
                    liste=liste_confirmee,
                    piece=piece,
                    quantite=item['quantite']
                )
                # ... (le reste de votre logique de confirmation)
            request.session['cart'] = {}
            messages.success(request, 'Votre liste a été confirmée et enregistrée.')
        else:
            messages.warning(request, 'Votre panier est vide.')
        return redirect('piece')
    return redirect('view_cart')

# Module planification
@login_required
def planification(request):
    User = get_user_model()
    user = request.user
    q = request.GET.get("q")

    # Filtrer les équipements basés sur la section de l'utilisateur
    if user.section == 'DISJONCTEUR':
        base_queryset = Equipement.objects.filter(type_equipement='Disjoncteur')
    elif user.section == 'TRANSFORMATEUR':
        base_queryset = Equipement.objects.filter(type_equipement='Transformateur')
    else:
        base_queryset = Equipement.objects.all()

    if q:
        # Recherche dans les centrales
        centrales = Centrale.objects.filter(
            Q(nom__icontains=q) | 
            Q(localisation__icontains=q)
        )
        
        # Recherche dans les équipements
        equipements_search = base_queryset.filter(
            Q(nom__icontains=q) | 
            Q(type_equipement__icontains=q) | 
            Q(numero_serie__icontains=q) | 
            Q(modèle__icontains=q) | 
            Q(marque__icontains=q)
        )
        
        # Ajouter les centrales des équipements trouvés
        centrales |= Centrale.objects.filter(equipement__in=equipements_search)
        
        # Précharger tous les équipements pour les centrales trouvées avec leurs planifications
        centrales = centrales.prefetch_related(
            Prefetch('equipement_set', 
                     queryset=base_queryset.prefetch_related('planification_set'),
                     to_attr='filtered_equipements')
        )
    else:
        centrales = Centrale.objects.prefetch_related(
            Prefetch('equipement_set', 
                     queryset=base_queryset.prefetch_related('planification_set'),
                     to_attr='filtered_equipements')
        )

    context = {
        "centrales": centrales
    }

    return render(request, "pages/planification/planification.html", context)


class AddPlanification(LoginRequiredMixin, CreateView):
    model = Planification
    form_class = PlanificationForm
    template_name = "pages/planification/add.html"

    def get_success_url(self):
        return reverse_lazy('planification') 

    def form_valid(self, form):
        response = super().form_valid(form)
        self.object = form.save()
        form = self.get_form()
        form = PlanificationForm()
        return response
 
@login_required
def update_planification(request, pk):
    planification = get_object_or_404(Planification, pk=pk)
    equipement = planification.equipement

    if request.method == 'POST':
        form = PlanificationForm(request.POST, instance=planification)
        if form.is_valid():
            form.save()
            messages.success(request, 'Planification mise à jour avec succès.')
            return redirect('planification')
    else:
        form = PlanificationForm(instance=planification)

    context = {
        'form': form,
        'planification': planification,
        'equipement': equipement
    }
    return render(request, 'pages/planification/update.html', context)

@login_required
def delete_planification(request, pk):
    planification = get_object_or_404(Planification, pk=pk)
    equipement = planification.equipement

    if request.method == 'POST':
        planification.delete()
        messages.success(request, 'Planification supprimée avec succès.')
        return redirect('planification')

    context = {
        'planification': planification,
        'equipement': equipement
    }
    return render(request, 'pages/planification/delete.html', context)


@csrf_protect
@require_POST
def save_planification_selection(request):
    try:
        data = json.loads(request.body)
        
        planification_id = data.get('planification_id')
        date_str = data.get('date')
        is_checked = data.get('is_checked')

        # Reste de votre logique de sauvegarde
        planification = Planification.objects.get(pk=planification_id)
        
        selection, created = PlanificationSelection.objects.get_or_create(
            planification=planification,
            date=date_str,
            defaults={'is_checked': is_checked}
        )

        if not created:
            selection.is_checked = is_checked
            selection.save()

        return JsonResponse({'status': 'success'})

    except Exception as e:
        return JsonResponse({
            'status': 'error', 
            'message': str(e)
        }, status=400)



#def planification_statistics(request):
    # Récupérer les statistiques de sélection
    #selections = PlanificationSelection.objects.filter(is_checked=True)
    
    # Grouper par planification, mois, année
    #statistics = selections.annotate(
        #month=ExtractMonth('date'),
        #year=ExtractYear('date')
    #).values('planification__tache', 'month', 'year') \
     #.annotate(checked_days=count('id'))

    #return render(request, 'statistics.html', {'statistics': statistics})

# Module Dossier de réchange
@login_required
def dossier(request):
    context = {}
    q = request.GET.get("q")
    base_queryset = Dossier.objects.all()

    if q:
        # Recherche Elasticsearch
        s = DossierDocument.search().query(
            ESQ("multi_match", 
                query=q, 
                fields=['nom', 'description']
            )
        )
        es_results = s.to_queryset()
        
        # Recherche Django ORM
        db_results = base_queryset.filter(
            Q(nom__icontains=q) | 
            Q(description__icontains=q) 
        )
        
        # Combiner les résultats
        liste_dossier = (es_results & base_queryset) | db_results
    else:
        liste_dossier = base_queryset

    context["liste_dossier"] = liste_dossier.distinct()
    return render(request, "pages/dossier/dossier.html", context)

@login_required
def detail_dossier(request, id_dossier):
    detail_dossier = Dossier.objects.get(id = id_dossier)
    context = {"dossier" : detail_dossier}
    return render(request, "pages/dossier/detail.html", context)

class AddDossier(LoginRequiredMixin, CreateView):
    model = Dossier
    form_class = DossierForm
    template_name = "pages/dossier/add.html"

    def get_success_url(self):
        return reverse_lazy('dossier') 

    def form_valid(self, form):
        response = super().form_valid(form)
        self.object = form.save()
        form = self.get_form()
        form = DossierForm()
        return response
 
class UpdateDossier(LoginRequiredMixin, UpdateView):
    model = Dossier
    form_class = DossierForm
    template_name = "pages/dossier/update.html"

    def get_success_url(self):
        return HttpResponse(reverse('dossier'))
    
    def get_object(self, queryset=None):
        return Dossier.objects.get(pk=self.kwargs['pk'])

class DeleteDossier(LoginRequiredMixin, DeleteView):
    model = Dossier
    template_name = "pages/dossier/delete.html"

    def get_success_url(self):
        return HttpResponse(reverse('dossier'))
    
    def get_object(self, queryset=None):
        return Dossier.objects.get(pk=self.kwargs['pk'])
    
