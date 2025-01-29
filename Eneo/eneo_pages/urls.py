from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from . import views

urlpatterns = [
    path("accueil/", views.home, name="home"),

    # Authentification
    path('', views.LoginView, name='login'),
    path('enregistrement/', views.RegisterView, name='register'),
    path('connexion/', views.LogoutView, name='logout'),
    path('mise-a-jour-profile/', views.update_profile, name='update_profile'),
    path('profile/', views.profile_view, name='profile'),
    path('setting/', views.setting_view, name='setting'),
    path('mot-de-passe-oublié/', views.ForgotPassword, name='forgot-password'),
    path('réinitialisation-mot-de-passe-envoyé/<str:reset_id>/', views.PasswordResetSent, name='password-reset-sent'),
    path('réinitialisation-mot-de-passe/<str:reset_id>/', views.ResetPassword, name='reset-password'),

    # Module Equipement
    path("equipement", views.equipement, name="equipement"),
    path("equipement/<int:id_equip>", views.detail_equipement, name="detail_equipement"),
    path("equipement/ajouter_un_equipement", views.AddEquipement.as_view(), name="ajouter_equipement"),
    path("equipement/update/<int:pk>", views.UpdateEquipement.as_view(), name="update_equipement"),
    path("equipement/delete/<int:pk>", views.DeleteEquipement.as_view(), name="delete_equipement"),
    path("equipement/import", views.importEquipement, name="equipement_import"),
    
    # Module Intervention
    path("intervention", views.intervention, name="intervention"),
    path("intervention/<int:id_intervention>", views.detail_intervention, name="detail_intervention"),
    path("intervention/ajouter", views.AddIntervention.as_view(), name="ajouter_intervention"),
    path("intervention/update/<int:pk>", views.UpdateIntervention.as_view(), name="update_intervention"),
    path("intervention/delete/<int:pk>", views.DeleteIntervention.as_view(), name="delete_intervention"),
    path('get_equipement/<int:intervention_id>/', views.get_equipement, name='get_equipement'),

    # Module pièce de réchange
    path("piece", views.piece, name="piece"),
    path("piece/<int:id_piece>", views.detail_piece, name="detail_piece"),
    path("piece/ajouter", views.AddPiece.as_view(), name="ajouter_piece"),
    path("piece/update/<int:pk>", views.UpdatePiece.as_view(), name="update_piece"),
    path("piece/delete/<int:pk>", views.DeletePiece.as_view(), name="delete_piece"),
    path("piece/cart", views.view_cart, name="view_cart"),
    path("add/<int:piece_id>/", views.add_to_cart, name="add_to_cart"),
    path('get_cart_quantity/', views.get_cart_quantity, name='get_cart_quantity'),
    path("remove/<int:piece_id>/", views.remove_from_cart, name="remove_from_cart"),
    path('confirm_cart/', views.confirm_cart, name='confirm_cart'),
    path('get_pieces_confirmees/<int:liste_id>/', views.get_pieces_confirmees, name='get_pieces_confirmees'),


    # Module Planification
    path("planification", views.planification, name="planification"),
    #path("planification/<int:id_planification>", views.detail_planification, name="detail_planification"),
    path("planification/ajouter", views.AddPlanification.as_view(), name="ajouter_planification"),
    path('planification/update/<int:pk>/', views.update_planification, name='update_planification'),
    path('planification/delete/<int:pk>/', views.delete_planification, name='delete_planification'),
    path('save-planification-selection/', views.save_planification_selection, name='save_planification_selection'),

    # Module dossier
    path("dossier", views.dossier, name="dossier"),
    path("dossier/<int:id_dossier>", views.detail_dossier, name="detail_dossier"),
    path("dossier/ajouter", views.AddDossier.as_view(), name="ajouter_dossier"),
    path("dossier/update/<int:pk>", views.UpdateDossier.as_view(), name="update_dossier"),
    path("dossier/delete/<int:pk>", views.DeleteDossier.as_view(), name="delete_dossier"),

]+ static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
