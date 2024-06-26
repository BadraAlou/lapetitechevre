from django.db import models

class Departement(models.Model):
    nom = models.CharField(max_length=100, unique=True)
    def __str__(self):
       return self.nom 
    
class Employe(models.Model):
    matricule = models.CharField(max_length=10, unique=True)
    nom = models.CharField(max_length=100)
    prenom = models.CharField(max_length=100)
    adresse = models.CharField(max_length=200)
    date_embauche = models.DateField()
    departement = models.ForeignKey('Departement', on_delete=models.CASCADE)
    def __str__(self):
        return f'{self.prenom} {self.nom}'
    
class Absence(models.Model):
    employe = models.ForeignKey(Employe, on_delete=models.CASCADE)
    date_debut = models.DateField()
    date_fin = models.DateField()
    raison = models.TextField()
    def __str__(self):
       return self.raison 
    
class Paiement(models.Model):
    employe = models.ForeignKey(Employe, on_delete=models.CASCADE)
    date_paiement = models.DateField()
    salaire = models.DecimalField(max_digits=10, decimal_places=2)
 
