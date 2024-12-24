from django.contrib.auth.models import AbstractUser, BaseUserManager, PermissionsMixin
from django.db import models
import uuid

class UserManager(BaseUserManager):
    def create_user(self, username, email, password=None, section=None, **extra_fields):
        if not email:
            raise ValueError('Users must have an email address')
        if not username:
            raise ValueError('Users must have a username')

        user = self.model(
            username=username,
            email=self.normalize_email(email),
            section=section,
            **extra_fields
        )
        user.set_password(password)  # Hash the password
        user.save(using=self._db)
        return user

    def create_superuser(self, username, email, password=None):
        user = self.create_user(
            username=username,
            email=email,
            password=password,
            section='ADMIN'  # Set default section for superuser
        )
        user.is_admin = True
        user.is_superuser = True
        user.is_staff = True
        user.save(using=self._db)
        return user
    
class User(AbstractUser, PermissionsMixin):
    class Section(models.TextChoices):
        ADMIN = "ADMIN", 'Admin'
        DISJONCTEUR = "DISJONCTEUR", 'Disjoncteur'
        TRANSFORMATEUR = "TRANSFORMATEUR", 'Transformateur'

    section = models.CharField(max_length=50, choices=Section.choices, default=Section.ADMIN)
    objects = UserManager()

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)


class Centrale(models.Model):
    nom=models.CharField(max_length=100)
    localisation = models.CharField(max_length=100)
    état = models.CharField(max_length=100)
    date_création=models.DateTimeField(auto_now_add=True)
    date_modification=models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.nom
    
class Equipement(models.Model):
    TYPE_EQUIPE = [
        ("Disjoncteur", "Disjoncteur",),
        ("Transformateur", "Transformateur"),
    ]
    centrale = models.ForeignKey(Centrale, on_delete=models.CASCADE)
    nom = models.CharField(max_length=100)
    type_equipement = models.CharField(max_length=100, choices=TYPE_EQUIPE)
    modèle = models.CharField(max_length=100)
    marque = models.CharField(max_length=100)
    puissance = models.FloatField()
    fréquence = models.FloatField()
    date_installation = models.DateField()
    #######Transformateurs#############
    fonction = models.CharField(max_length=100, blank=True, null=True)
    emplacement_couplage = models.CharField(max_length=100, blank=True, null=True)
    regleur_en_chargeur = models.CharField(max_length=100, blank=True, null=True)
    mode_de_fonctionnement = models.CharField(max_length=100, blank=True, null=True)
    #######Disjoncteurs#################
    technique_de_coupure = models.CharField(max_length=100, blank=True, null=True)
    pouvoir_de_coupure = models.CharField(max_length=100, blank=True, null=True)
    pression_gaz_nombre_de_pôle  = models.CharField(max_length=100, blank=True, null=True)
    courant_nominal_en_service_continu = models.CharField(max_length=100, blank=True, null=True)
    numero_service = models.CharField(max_length=100, blank=True, null=True)
    tension_assigne = models.CharField(max_length=100, blank=True, null=True)
    pouvoir_de_coupure_nominal_court_circuit = models.CharField(max_length=100, blank=True, null=True)
    pouvoir_de_fermeture_nominal_court_circuit  = models.CharField(max_length=100, blank=True, null=True)
    date_création=models.DateTimeField(auto_now_add=True)
    date_modification=models.DateTimeField(auto_now=True)

    def __str__(self):
        return "{} {}".format(self.nom, self.type_equipement)

class Intervention(models.Model):
    STATUS = [
        ("En panne", "En panne"),
        ("Encours", "Encours de dépannage"),
        ("Rétablir", "Rétablir"),
    ]
    equipement = models.ForeignKey(Equipement, on_delete=models.CASCADE)
    date_intervention=models.DateField()
    date_defaillance=models.DateField()
    description = models.TextField(blank=True, null=True)
    tache_maintenance = models.TextField(blank=True, null=True)
    responsable = models.CharField(max_length=100, blank=True, null=True)
    status = models.CharField(max_length=100, choices=STATUS)
    coût = models.IntegerField()
    date_création=models.DateTimeField(auto_now_add=True)
    date_modification=models.DateTimeField(auto_now=True)

    def __str__(self):
        return "{} {}".format(self.id, self.equipement)
    
class Pièce(models.Model):
    nom=models.CharField(max_length=100)
    description = models.TextField()
    photo = models.ImageField(upload_to="image", blank=True, null=True)
    quantité_disponible = models.IntegerField()
    prix_unitaire = models.IntegerField()
    date_création=models.DateTimeField(auto_now_add=True)
    date_modification=models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.nom


class PasswordReset(models.Model):
    utilisateur = models.ForeignKey(User, on_delete=models.CASCADE)
    id_modification = models.UUIDField(default=uuid.uuid4, unique=True, editable=False)
    date_création = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Password reset for {self.user.username} at {self.date_création}"