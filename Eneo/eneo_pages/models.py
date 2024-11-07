from django.db import models

# Create your models here.
#()
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
        ("Disjoncteurs", "Disjoncteurs",),
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
    fonction = models.CharField(max_length=100)
    emplacement_couplage = models.CharField(max_length=100)
    regleur_en_chargeur = models.CharField(max_length=100)
    mode_de_fonctionnement = models.CharField(max_length=100)
    #######Disjoncteurs#################
    technique_de_coupure = models.CharField(max_length=100)
    pouvoir_de_coupure = models.CharField(max_length=100)
    pression_gaz_nombre_de_pôle  = models.CharField(max_length=100)
    courant_nominal_en_service_continu = models.CharField(max_length=100)
    numero_service = models.CharField(max_length=100)
    tension_assigne = models.CharField(max_length=100)
    pouvoir_de_coupure_nominal_court_circuit = models.CharField(max_length=100)
    pouvoir_de_fermeture_nominal_court_circuit  = models.CharField(max_length=100)
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
    description = models.TextField()
    responsable = models.CharField(max_length=100)
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