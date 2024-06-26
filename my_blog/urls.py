from django.contrib import admin
from django.urls import path
from django.conf import settings 
from django.conf.urls.static import static
from django.contrib.auth.views import LoginView
from blog.views import (
    fromage, home, detail, liste_commandes, formulaire_contact, register, 
    user_login, custom_logout, acheter_article, confirmation_achat, connexion_reussie, 
    message_list, delete_message, entreprise, achat_reussie, annuler_commande, 
    annulation_reussie, supprimer_panier, ajouter_au_panier, panier, membres,
    confirmation_achat_panier, telechargez_facture, telecharger_facture, panier_validez, 
    stock_insuffisant, historique_commandes, modifier_quantite_panier,
    CustomPasswordResetView, CustomPasswordResetDoneView, CustomPasswordResetConfirmView, CustomPasswordResetCompleteView
)

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', fromage, name="fromage"),
    path('home/', home, name="home"),
    path('article/<int:id_article>/', detail, name="detail"),
    path('commandes/', liste_commandes, name='liste_commandes'),
    path('contact/', formulaire_contact, name='formulaire_contact'),
    path('register/', register, name='register'),
    path('login/', user_login, name='login'),
    path('logout/', custom_logout, name='logout'),  # Définissez l'URL de déconnexion ici
    path('acheter/<int:id_article>/', acheter_article, name='acheter_article'),
    path('confirmation-achat/<int:commande_id>/', confirmation_achat, name='confirmation_achat'),
    path('connexion-reussie/', connexion_reussie, name='connexion_reussie'),
    path('message_list/', message_list, name='message_list'),
    path('delete_message/<int:message_id>/', delete_message, name='delete_message'),
    path('entreprise/', entreprise, name='entreprise'),
    path('achat_reussie/<int:commande_id>/', achat_reussie, name='achat_reussie'),
    path('annuler_commande/<int:commande_id>/', annuler_commande, name='annuler_commande'),
    path('annulation_reussie/', annulation_reussie, name='annulation_reussie'),
    path('panier/', panier, name='panier'),  # Chemin pour la vue du panier
    path('supprimer_panier/<int:id_ligne>/', supprimer_panier, name='supprimer_panier'),
    path('ajouter-au-panier/<int:id_article>/', ajouter_au_panier, name='ajouter_au_panier'),
    path('membres/', membres, name='membres'),
    path('accounts/login/', LoginView.as_view(template_name='login.html'), name='login'),
    path('confirmation_achat_panier/', confirmation_achat_panier, name='confirmation_achat_panier'),
    path('telechargez_facture/', telechargez_facture, name='telechargez_facture'),
    path('telecharger_facture/<int:commande_id>/', telecharger_facture, name='telecharger_facture'),
    path('panier_validez/', panier_validez, name='panier_validez'),
    path('stock_insuffisant/', stock_insuffisant, name='stock_insuffisant'),
    path('historique-commandes/', historique_commandes, name='historique_commandes'),
    path('modifier_quantite_panier/<int:id_ligne>/', modifier_quantite_panier, name='modifier_quantite_panier'),
    path('password_reset/', CustomPasswordResetView.as_view(), name='password_reset'),
    path('password_reset/done/', CustomPasswordResetDoneView.as_view(), name='password_reset_done'),
    path('reset/<uidb64>/<token>/', CustomPasswordResetConfirmView.as_view(), name='password_reset_confirm'),
    path('reset/done/', CustomPasswordResetCompleteView.as_view(), name='password_reset_complete'),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
