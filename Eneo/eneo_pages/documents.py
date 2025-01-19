from django_elasticsearch_dsl import Document
from django_elasticsearch_dsl.registries import registry
from .models import *

@registry.register_document
class CentraleDocument (Document):
    class Index:
        name = "centrales"
        settings = {"number_of_shards": 1, "number_of_replicas": 0}
    class Django:
        model = Centrale
        fields = ["nom", "localisation", "état"]

@registry.register_document
class EquipementDocument (Document):
    class Index:
        name = "equipements"
        settings = {"number_of_shards": 1, "number_of_replicas": 0}
    class Django:
        model = Equipement
        fields = ["nom", "type_equipement", "numero_serie", "modèle", "marque"]

@registry.register_document
class PièceDocument (Document):
    class Index:
        name = "pièces"
        settings = {"number_of_shards": 1, "number_of_replicas": 0}
    class Django:
        model = Pièce
        fields = ["nom", "description", "fournisseur"]

@registry.register_document
class InterventionDocument (Document):
    class Index:
        name = "interventions"
        settings = {"number_of_shards": 1, "number_of_replicas": 0}
    class Django:
        model = Intervention
        fields = ["type_intervention", "responsable", "status", "description", "tache_maintenance", "action_correctives", "causes_profondes"]

@registry.register_document
class DossierDocument (Document):
    class Index:
        name = "dossiers"
        settings = {"number_of_shards": 1, "number_of_replicas": 0}
    class Django:
        model = Dossier
        fields = ["nom", "description"]