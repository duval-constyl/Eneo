from django.urls import path, include
from . import views

urlpatterns = [
    path("", views.home, name="home"),
    path("equipement", views.equipement, name="equipement"),
    path("intervention", views.intervention, name="intervention"),
    path("piece", views.piece, name="piece")
]