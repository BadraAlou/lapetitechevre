from django.db import models
from django.contrib.auth.models import User
from django import forms  # Ajoutez cette ligne pour importer le module forms
from django.db import models
from django.contrib.auth.models import User

# Votre code de modèles ici

class ContactForm(forms.Form):
    name = forms.CharField(label='Nom', widget=forms.TextInput(attrs={'class': 'form-control'}))
    email = forms.EmailField(label='Email', widget=forms.EmailInput(attrs={'class': 'form-control'}))
    subject = forms.CharField(label='Sujet', widget=forms.TextInput(attrs={'class': 'form-control'}))
    message = forms.CharField(label='Message', widget=forms.Textarea(attrs={'class': 'form-control'}))


class Category(models.Model):  # Renommez la classe en Category au lieu de category
    name = models.CharField(max_length=120)

    def __str__(self):
        return self.name

from django.db import models
from django.db.models.signals import post_save, post_delete
from django.dispatch import receiver

class Category(models.Model):
    name = models.CharField(max_length=50)
    
    def __str__(self):
        return self.name

class Article(models.Model):
    title = models.CharField(max_length=50)
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    desc = models.TextField()
    image = models.ImageField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    prix = models.DecimalField(max_digits=10, decimal_places=2)
    stock = models.PositiveIntegerField(default=0)
    modes_paiement = models.CharField(max_length=100, choices=[
        ('orange_money', 'Orange Money'),
        ('money_gram', 'Money Gram'),
        ('carte_visa', 'Carte Visa')
    ])

    def __str__(self):
        return self.title

    def is_out_of_stock(self):
        return self.stock == 0

class StockEpuisé(models.Model):
    article = models.OneToOneField(Article, on_delete=models.CASCADE)

    def __str__(self):
        return f"Article en rupture de stock : {self.article.title}"

@receiver(post_save, sender=Article)
def update_stock_epuise(sender, instance, **kwargs):
    if instance.stock == 0:
        StockEpuisé.objects.get_or_create(article=instance)
    else:
        StockEpuisé.objects.filter(article=instance).delete()

@receiver(post_delete, sender=Article)
def delete_stock_epuise(sender, instance, **kwargs):
    StockEpuisé.objects.filter(article=instance).delete()



class Panier(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)

    def __str__(self):
        return f"Panier de {self.user.username}"

from django.db import models

class LignePanier(models.Model):
    panier = models.ForeignKey(Panier, on_delete=models.CASCADE)
    article = models.ForeignKey(Article, on_delete=models.CASCADE)
    quantite = models.PositiveIntegerField()
    prix_unitaire = models.DecimalField(max_digits=10, decimal_places=2)
    

    @property
    def prix_total(self):
        return self.quantite * self.prix_unitaire

    def __str__(self):
        return f"{self.quantite} x {self.article.title} (Panier de {self.panier.user.username})"



class Commande(models.Model):
    nom_client = models.CharField(max_length=255)
    produit = models.CharField(max_length=255)
    quantite = models.IntegerField()
    prix_unitaire = models.DecimalField(max_digits=10, decimal_places=2)
    total = models.DecimalField(max_digits=10, decimal_places=2)
    numero_telephone = models.CharField(max_length=20, blank=True, null=True)
    adresse = models.TextField()
    CHOIX_MODE_PAIEMENT = [
        ('orange_money', 'Orange Money'),
        ('money_gram', 'Money Gram'),
        ('carte_visa', 'Carte Visa'),
    ]
    
    modes_paiement = models.CharField(max_length=20, choices=CHOIX_MODE_PAIEMENT)

class Contact(models.Model):
    nom = models.CharField(max_length=100)
    email = models.EmailField()
    message = models.TextField()

class ContactForm(forms.Form):
    name = forms.CharField(label='Nom', widget=forms.TextInput(attrs={'class': 'form-control'}))
    email = forms.EmailField(label='Email', widget=forms.EmailInput(attrs={'class': 'form-control'}))
    subject = forms.CharField(label='Sujet', widget=forms.TextInput(attrs={'class': 'form-control'}))
    message = forms.CharField(label='Message', widget=forms.Textarea(attrs={'class': 'form-control'}))

class Message(models.Model):
    name = models.CharField(max_length=100)
    email = models.EmailField()
    message = models.TextField()
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.name} - {self.email} - {self.timestamp}"

class ConnexionLog(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    timestamp = models.DateTimeField(auto_now_add=True)
    action = models.CharField(max_length=20)  # 'connexion' ou 'deconnexion'

    class Meta:
        ordering = ['-timestamp']


from django.db import models

class Membre(models.Model):
    nom = models.CharField(max_length=100)
    email = models.EmailField()
    numero = models.CharField(max_length=15)
    poste = models.CharField(max_length=100)
    photo = models.ImageField(upload_to='photos/')

    def __str__(self):
        return self.nom
from django.db import models
from django.contrib.auth.models import User
from .models import Panier, LignePanier

class CommandeConfirmee(models.Model):
    utilisateur = models.ForeignKey(User, on_delete=models.CASCADE)
    panier = models.ForeignKey(Panier, on_delete=models.CASCADE)
    lignes_panier = models.ManyToManyField(LignePanier)
    date_commande = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Commande de {self.panier.user.username} - {self.date_commande}"

from django.db import models
from .models import Commande

class Facture(models.Model):
    commande = models.ForeignKey(Commande, on_delete=models.CASCADE)
    contenu_pdf = models.BinaryField()  # Champ binaire pour stocker le contenu PDF
    nom_client = models.CharField(max_length=100, default='')
    adresse = models.TextField(blank=True, null=True)
    quantite = models.IntegerField(default=0)
    prix_unitaire = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    total = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    numero_telephone = models.CharField(max_length=20, blank=True, null=True)
    
    CHOIX_MODE_PAIEMENT = [
        ('orange_money', 'Orange Money'),
        ('money_gram', 'Money Gram'),
        ('carte_visa', 'Carte Visa'),
    ]
    modes_paiement = models.CharField(max_length=20, choices=CHOIX_MODE_PAIEMENT, default='orange_money')

    def save(self, *args, **kwargs):
        if not self.nom_client:
            # Récupérer le nom d'utilisateur actuel
            self.nom_client = self.commande.user.username if self.commande.user else ''
        super().save(*args, **kwargs)

    def __str__(self):
        return f"Facture pour la commande {self.commande.id}"
    from django.db import models
from django.contrib.auth.models import User
from .models import Article

class CommandeHistorique(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    produit = models.ForeignKey(Article, on_delete=models.CASCADE)
    quantite = models.PositiveIntegerField()
    prix_unitaire = models.DecimalField(max_digits=10, decimal_places=2)
    total = models.DecimalField(max_digits=10, decimal_places=2)
    date_commande = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user.username} - {self.produit.title} - {self.date_commande}"
