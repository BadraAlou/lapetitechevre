from django.contrib import admin
from .models import Article, Category, Commande, Contact, ConnexionLog,Membre,Panier,CommandeConfirmee,Facture,StockEpuisé,CommandeHistorique

# Enregistrez vos modèles ici
admin.site.register(Article)
admin.site.register(Category)
admin.site.register(Commande)
admin.site.register(Contact)
admin.site.register(ConnexionLog)
admin.site.register(Membre)
admin.site.register(Panier)
admin.site.register(CommandeConfirmee)
admin.site.register(Facture)
admin.site.register(StockEpuisé)
admin.site.register(CommandeHistorique)