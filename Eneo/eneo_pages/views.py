from datetime import datetime
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import redirect, render
from django.urls import reverse, reverse_lazy
from django.views.generic.edit import CreateView,UpdateView,DeleteView
from django.contrib.auth.mixins import LoginRequiredMixin
from .models import *
from .forms import *
from .resources import *
from django.contrib import messages
from openpyxl import load_workbook
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.conf import settings
from django.core.mail import EmailMessage
from django.utils import timezone
from django.contrib.auth import login, get_user_model


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
    User = get_user_model()  # Get the custom user model
    user = request.user  # Get the currently logged-in user
    # Filter equipment based on user section
    if user.section == 'DISJONCTEUR':
        liste_equipement = Equipement.objects.filter(type_equipement='Disjoncteur')
    elif user.section == 'TRANSFORMATEUR':
        liste_equipement = Equipement.objects.filter(type_equipement='Transformateur')
    else:
        liste_equipement = Equipement.objects.all()

    context = {"liste_equipement" : liste_equipement}
    
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

@login_required  
def importEquipement(request):
    if request.method == 'POST':
        excel_file = request.FILES['excel_file']
        wb = load_workbook(excel_file)
        ws = wb.active

        for row in ws.iter_rows(min_row=19, values_only=True):
            centrale_nom = row[0]  # Nom de la centrale dans la première colonne du fichier
            # Trouver ou créer l'instance de Centrale en fonction du nom
            centrale_instance, created = Centrale.objects.get_or_create(nom=centrale_nom)
            Equipement.objects.create(
                centrale=centrale_instance,
                nom=row[1],
                type_equipement=row[2],
                modele=row[3],
                marque=row[4],
                puissance=row[5],
                frequence=row[6],
                date_installation=datetime.strptime(row[7], '%Y-%m-%d') if row[7] else None,
                fonction=row[8],
                emplacement_couplage=row[9],
                regleur_en_chargeur=row[10],
                mode_de_fonctionnement=row[11],
                technique_de_coupure=row[12],
                pouvoir_de_coupure=row[13],
                pression_gaz_nombre_de_pole=row[14],
                courant_nominal_en_service_continu=row[15],
                numero_service=row[16],
                tension_assigne=row[17],
                pouvoir_de_coupure_nominal_court_circuit=row[18],
                pouvoir_de_fermeture_nominal_court_circuit=row[19]
            )
        return render(request, 'pages/equipement.html')
    return render(request, 'base/import.html')

# Module Intervention
@login_required
def intervention(request):
    User = get_user_model()  # Get the custom user model
    user = request.user  # Get the currently logged-in user
    
    # Filter equipment based on user section
    if user.section == 'DISJONCTEUR':
        intervention = Intervention.objects.filter(equipement__type_equipement='Disjoncteur')
    elif user.section == 'TRANSFORMATEUR':
        intervention = Intervention.objects.filter(equipement__type_equipement='Transformateur')
    else:
        intervention = Intervention.objects.all()

    context = {"liste_intervention" : intervention}
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
    form_class = InterventionForm
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
    piece = Pièce.objects.all()
    context = {"liste_piece" : piece}
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


# Module Planification
@login_required
def planification(request):
    piece = Pièce.objects.all()
    context = {"liste_piece" : piece}
    return render(request, "pages/planification/planification.html", context)

@login_required
def detail_planification(request, id_planification):
    detail_piece = Pièce.objects.get(id = id_planification)
    context = {"piece" : detail_piece}
    return render(request, "pages/planification/detail.html", context)

class AddPlanification(LoginRequiredMixin, CreateView):
    model = Pièce
    form_class = PieceForm
    template_name = "pages/planification/add.html"

    def get_success_url(self):
        return reverse_lazy('planification') 

    def form_valid(self, form):
        response = super().form_valid(form)
        self.object = form.save()
        form = self.get_form()
        form = PieceForm()
        return response
 
class UpdatePlanification(LoginRequiredMixin, UpdateView):
    model = Pièce
    form_class = PieceForm
    template_name = "pages/planification/update.html"

    def get_success_url(self):
        return HttpResponseRedirect('planification') 
    
    def get_object(self, queryset=None):
        return Pièce.objects.get(pk=self.kwargs['pk'])

class DeletePlanification(LoginRequiredMixin, DeleteView):
    model = Pièce
    template_name = "pages/planification/delete.html"

    def get_success_url(self):
        return HttpResponseRedirect('planification')  
    
    def get_object(self, queryset=None):
        return Pièce.objects.get(pk=self.kwargs['pk'])
