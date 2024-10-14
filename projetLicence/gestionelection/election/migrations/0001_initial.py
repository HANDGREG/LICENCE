# Generated by Django 5.1.2 on 2024-10-14 13:06

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='BureauDeVote',
            fields=[
                ('id_bureau', models.AutoField(primary_key=True, serialize=False)),
                ('nom', models.CharField(max_length=100, unique=True)),
                ('adresse', models.CharField(max_length=255)),
                ('arrondissement', models.CharField(max_length=50)),
            ],
            options={
                'verbose_name': 'BureauVote',
                'verbose_name_plural': 'BureauVote',
                'db_table': 'BureauVote',
                'managed': True,
            },
        ),
        migrations.CreateModel(
            name='Candidat',
            fields=[
                ('code_candidat', models.CharField(max_length=10, primary_key=True, serialize=False, unique=True)),
                ('nom', models.CharField(max_length=100)),
                ('prenom', models.CharField(max_length=100)),
                ('parti', models.CharField(max_length=100, unique=True)),
                ('desciption', models.TextField()),
                ('email', models.EmailField(max_length=254, unique=True)),
                ('date_enregistrement', models.DateTimeField(auto_now_add=True)),
                ('image', models.ImageField(unique=True, upload_to='images/candidat')),
            ],
            options={
                'verbose_name': 'Candidat',
                'verbose_name_plural': 'Candidat',
                'db_table': 'Candidat',
                'managed': True,
            },
        ),
        migrations.CreateModel(
            name='Electeur',
            fields=[
                ('code_electeur', models.CharField(max_length=10, primary_key=True, serialize=False, unique=True)),
                ('nom', models.CharField(max_length=100)),
                ('prenom', models.CharField(max_length=100)),
                ('date_naissance', models.DateField()),
                ('adresse', models.CharField(max_length=255)),
                ('telephone', models.CharField(default='+237', max_length=20, unique=True)),
                ('email', models.EmailField(max_length=254, unique=True)),
                ('date_enregistrement', models.DateTimeField(auto_now_add=True)),
                ('arrondissement', models.CharField(max_length=50)),
                ('image', models.ImageField(unique=True, upload_to='images/electeur')),
                ('mot_de_passe', models.CharField(default='123', max_length=128)),
                ('actif', models.BooleanField(default=True)),
            ],
            options={
                'verbose_name': 'Electeur',
                'verbose_name_plural': 'Electeur',
                'db_table': 'Electeur',
                'managed': True,
            },
        ),
        migrations.CreateModel(
            name='Resultat',
            fields=[
                ('id_resultat', models.AutoField(primary_key=True, serialize=False)),
                ('nombre_votes', models.IntegerField(default=0)),
                ('date', models.DateTimeField(auto_now_add=True)),
                ('pourcentage', models.DecimalField(decimal_places=2, max_digits=5)),
                ('bureau', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='election.bureaudevote')),
                ('candidat', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='election.candidat')),
            ],
            options={
                'verbose_name': 'Resultat',
                'verbose_name_plural': 'Resultat',
                'db_table': 'Resultat',
                'managed': True,
            },
        ),
        migrations.CreateModel(
            name='TotalVotes',
            fields=[
                ('id_total_votes', models.AutoField(primary_key=True, serialize=False)),
                ('nombre_votes', models.IntegerField(default=0)),
                ('pourcentage', models.DecimalField(decimal_places=2, max_digits=5)),
                ('candidat', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to='election.candidat')),
            ],
            options={
                'verbose_name': 'TotalVotes',
                'verbose_name_plural': 'TotalVotes',
                'db_table': 'TotalVotes',
                'managed': True,
            },
        ),
        migrations.CreateModel(
            name='Vote',
            fields=[
                ('id_vote', models.AutoField(primary_key=True, serialize=False)),
                ('date_vote', models.DateTimeField(auto_now_add=True)),
                ('bureau', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='election.bureaudevote')),
                ('candidat', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='candidat', to='election.candidat')),
                ('electeur', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='vote_electeur', to='election.electeur', unique=True)),
            ],
            options={
                'verbose_name': 'Vote',
                'verbose_name_plural': 'Vote',
                'db_table': 'Vote',
            },
        ),
    ]
