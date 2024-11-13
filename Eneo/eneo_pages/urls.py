from django.urls import path, include
from . import views

urlpatterns = [
    path("", views.home, name="home"),
    path("equipement", views.equipement, name="equipement"),
    path("equipement/<int:id_equip>", views.detail_equipement, name="detail_equipement"),
    path("equipement/ajouter_un_equipement", views.AddEquipement.as_view(), name="ajouter_equipement"),
    path("equipement/update/<int:pk>", views.UpdateEquipement.as_view(), name="update_equipement"),
    path("equipement/delete/<int:pk>", views.DeleteEquipement.as_view(), name="delete_equipement"),
    path("equipement/import", views.importEquipement, name="equipement_import"),
    path("intervention", views.intervention, name="intervention"),
    path("piece", views.piece, name="piece")
]