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
    path("intervention/<int:id_intervention>", views.detail_intervention, name="detail_intervention"),
    path("intervention/ajouter", views.AddIntervention.as_view(), name="ajouter_intervention"),
    path("intervention/update/<int:pk>", views.UpdateIntervention.as_view(), name="update_intervention"),
    path("intervention/delete/<int:pk>", views.DeleteIntervention.as_view(), name="delete_intervention"),
    path("piece", views.piece, name="piece")
]