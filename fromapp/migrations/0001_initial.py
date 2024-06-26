# Generated by Django 5.0.1 on 2024-06-22 00:36

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Departement',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nom', models.CharField(max_length=100, unique=True)),
            ],
        ),
        migrations.CreateModel(
            name='Employe',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('matricule', models.CharField(max_length=10, unique=True)),
                ('nom', models.CharField(max_length=100)),
                ('prenom', models.CharField(max_length=100)),
                ('adresse', models.CharField(max_length=200)),
                ('date_embauche', models.DateField()),
                ('departement', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='fromapp.departement')),
            ],
        ),
        migrations.CreateModel(
            name='Absence',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('date_debut', models.DateField()),
                ('date_fin', models.DateField()),
                ('raison', models.TextField()),
                ('employe', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='fromapp.employe')),
            ],
        ),
        migrations.CreateModel(
            name='Paiement',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('date_paiement', models.DateField()),
                ('salaire', models.DecimalField(decimal_places=2, max_digits=10)),
                ('employe', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='fromapp.employe')),
            ],
        ),
    ]