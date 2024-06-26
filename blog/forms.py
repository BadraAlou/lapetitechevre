# forms.py
from django.contrib.auth.forms import AuthenticationForm

class AuthenticationForm(AuthenticationForm):
    pass
from django import forms

class CommandeForm(forms.Form):
    nom_client = forms.CharField(label='Nom', max_length=100)
    produit = forms.CharField(label='Produit', max_length=200)
    quantite = forms.IntegerField(label='Quantité')
    prix_unitaire = forms.DecimalField(label='Prix unitaire', max_digits=10, decimal_places=2)
    total = forms.DecimalField(label='Total', max_digits=10, decimal_places=2)
    modes_paiement = forms.ChoiceField(label='Mode de paiement', choices=[
        ('orange_money', 'Orange Money'),
        ('money_gram', 'Money Gram'),
        ('carte_visa', 'Carte Visa')
    ], required=False)
    numero_telephone = forms.CharField(label='Numéro de téléphone', max_length=20, required=False)
    adresse = forms.CharField(label='Adresse', widget=forms.Textarea, required=False)
from django import forms

from django import forms

class AjouterAuPanierForm(forms.Form):
    quantite = forms.IntegerField(min_value=1, initial=1, label='Quantité')




