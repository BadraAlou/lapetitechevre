from django.contrib import admin

from django.contrib.admin.models import LogEntry

# Register your models here.
from .models import *

class LogEntryAdmin(admin.ModelAdmin):
    list_display = ['action_time', 'user', 'content_type', 'object_repr', 'action_flag']
    list_filter = ('content_type',)
    search_fields = ('user__username',)
    date_hierarchy = 'action_time'

class DepartementAdmin(admin.ModelAdmin):
    list_display = ('nom',)
    search_fields = ('nom', )
    list_filter = ('nom',)

class EmployeAdmin(admin.ModelAdmin):
    list_display = ('matricule', 'nom', 'prenom', 'adresse' ,'departement', 'date_embauche')
    search_fields = ('matricule', 'nom', 'prenom')
    list_filter = ('departement', 'date_embauche')


class AbsenceAdmin(admin.ModelAdmin):
    list_display = ('employe', 'date_debut', 'date_fin', 'raison')
    search_fields = ('employe__nom', 'employe__matricule')
    list_filter = ('date_debut', 'date_fin')

class PaiementAdmin(admin.ModelAdmin):
    list_display = ('employe', 'date_paiement', 'salaire')
    search_fields = ('employe__nom', 'employe__matricule', 'salaire')
    list_filter = ( 'salaire',)

admin.site.register(Employe, EmployeAdmin)
admin.site.register(Departement, DepartementAdmin)
admin.site.register(Absence, AbsenceAdmin)
admin.site.register(Paiement, PaiementAdmin)
admin.site.register(LogEntry, LogEntryAdmin)

admin.site.site_header ='Gestion Dentreprise'
admin.site.site_header ='Gestion Dentreprise'
admin.site.site_title = 'Administration E-Commerce '