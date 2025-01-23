from django.contrib import admin
from .models import *

# Register your models here.
#()
admin.site.register(Centrale)
admin.site.register(Equipement)
admin.site.register(Intervention)
admin.site.register(Pièce)
admin.site.register(PasswordReset)
admin.site.register(User)
admin.site.register(Dossier)
admin.site.register(Utiliser)
admin.site.register(ListePieceConfirmee)
admin.site.register(PieceConfirmee)
admin.site.register(Planification)
admin.site.register(PlanificationSelection)

