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
