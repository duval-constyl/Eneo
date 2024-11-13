from import_export import resources
from .models import *


class EquipementResources(resources.ModelResource):
    class meta:
        model = Equipement