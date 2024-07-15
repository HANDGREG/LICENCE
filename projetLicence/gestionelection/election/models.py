from django.db import models
from django.core.exceptions import ValidationError
from django.contrib.auth.hashers import make_password, check_password

# Create your models here.



class Electeur(models.Model):
    code_electeur = models.CharField(max_length=10, unique=True,primary_key=True)
    nom = models.CharField(max_length=100)
    prenom = models.CharField(max_length=100)
    date_naissance = models.DateField()
    adresse = models.CharField(max_length=255)
    telephone = models.CharField(max_length=20,default='+237', unique=True)
    email = models.EmailField(unique=True)
    date_enregistrement = models.DateTimeField(auto_now_add=True)
    arrondissement=models.CharField(max_length=50)
    image=models.ImageField(upload_to='images/electeur', blank=False , unique=True)
    mot_de_passe = models.CharField(max_length=128, blank=False,default='123')
    actif=models.BooleanField(default=True)


    def trouver_bureau_vote(self):
        """
        Trouve le bureau de vote correspondant à l'arrondissement ou à l'adresse de l'électeur.
        """
        # Recherche par arrondissement ou adresse
        bureaux = BureauDeVote.objects.filter(
            models.Q(arrondissement=self.arrondissement) | 
            models.Q(adresse=self.adresse)
        )
        if bureaux:

            return bureaux
        else:
           return None
    

    class  Meta:
        db_table = 'Electeur'
        managed = True
        verbose_name = 'Electeur'
        verbose_name_plural = 'Electeur'

    def clean(self):
        """
        Nettoie et valide les données avant de sauvegarder.
        """
        if not self.mot_de_passe:
            raise ValidationError('Le mot de passe est obligatoire.')

        # Validation de la longueur et des caractères du mot de passe
        if len(self.mot_de_passe) < 8:
            raise ValidationError('Le mot de passe doit contenir au moins 8 caractères.')
        if not any(char.isdigit() for char in self.mot_de_passe):
            raise ValidationError('Le mot de passe doit contenir au moins un chiffre.')
        if not any(char.isalpha() for char in self.mot_de_passe):
            raise ValidationError('Le mot de passe doit contenir au moins une lettre.')

    def save(self, *args, **kwargs):
        """
        Chiffre le mot de passe avant de sauvegarder.
        """
        # Si le mot de passe n'est pas déjà haché, le hacher
        if not check_password(self.mot_de_passe, self.mot_de_passe):
            self.mot_de_passe = make_password(self.mot_de_passe)
        
        # Appeler la méthode de sauvegarde de la classe parente
        super(Electeur, self).save(*args, **kwargs)

    def __str__(self):
        return f"{self.nom} {self.prenom}"



class Candidat(models.Model):
    
    code_candidat = models.CharField(max_length=10, unique=True,primary_key=True)
    nom = models.CharField(max_length=100)
    prenom = models.CharField(max_length=100)
    parti = models.CharField(max_length=100, unique=True)
    desciption = models.TextField()
    email = models.EmailField( unique=True)
    date_enregistrement = models.DateTimeField(auto_now_add=True)
    image=models.ImageField(upload_to='images/candidat', blank=False, unique=True)

    class  Meta:
        db_table = 'Candidat'
        managed = True
        verbose_name = 'Candidat'
        verbose_name_plural = 'Candidat'



    def __str__(self):
        return f"{self.nom} {self.prenom}"

class BureauDeVote(models.Model):
    id_bureau = models.AutoField(primary_key=True)
    nom = models.CharField(max_length=100, unique=True)
    adresse = models.CharField(max_length=255)
    arrondissement=models.CharField(max_length=50)

    def __str__(self):
        return self.nom
    
    class  Meta:
        db_table = 'BureauVote'
        managed = True
        verbose_name = 'BureauVote'
        verbose_name_plural = 'BureauVote'



class Vote(models.Model):
    id_vote = models.AutoField(primary_key=True)
    electeur = models.ForeignKey(Electeur, related_name="vote_electeur", null=True, blank=True, on_delete=models.SET_NULL, unique=True)
    candidat = models.ForeignKey(Candidat, related_name="candidat", on_delete=models.CASCADE)
    bureau = models.ForeignKey(BureauDeVote, on_delete=models.CASCADE)
    date_vote = models.DateTimeField(auto_now_add=True)
   
    
    def update_resultat(self):
        total_votes_bureau = Vote.objects.filter(bureau=self.bureau).count()
        candidats = Candidat.objects.all()
        for candidat in candidats:
            votes_candidat_bureau = Vote.objects.filter(bureau=self.bureau, candidat=candidat).count()
            pourcentage = (votes_candidat_bureau / total_votes_bureau) * 100 if total_votes_bureau > 0 else 0
            Resultat.objects.update_or_create(
                bureau=self.bureau,
                candidat=candidat,
                defaults={'nombre_votes': votes_candidat_bureau, 'pourcentage': pourcentage}
            )

    def update_total_votes(self):
        candidats = Candidat.objects.all()
        total_votes_all = Vote.objects.count()
        for candidat in candidats:
            votes_candidat = Vote.objects.filter(candidat=candidat).count()
            pourcentage = (votes_candidat / total_votes_all) * 100 if total_votes_all > 0 else 0
            TotalVotes.objects.update_or_create(
                candidat=candidat,
                defaults={'nombre_votes': votes_candidat, 'pourcentage': pourcentage}
            )

    def save(self, *args, **kwargs):
        super(Vote, self).save(*args, **kwargs)
        self.update_resultat()
        self.update_total_votes()
    def __str__(self):
        return f"Vote de {self.electeur} pour {self.candidat} à {self.bureau}"
    class Meta:
        db_table = 'Vote'
        verbose_name = 'Vote'
        verbose_name_plural = 'Vote'



class Resultat(models.Model):
    id_resultat = models.AutoField(primary_key=True)
    bureau = models.ForeignKey(BureauDeVote, on_delete=models.CASCADE)
    candidat = models.ForeignKey(Candidat, on_delete=models.CASCADE)
    nombre_votes = models.IntegerField(default=0)
    date = models.DateTimeField(auto_now_add=True)
    pourcentage = models.DecimalField(max_digits=5, decimal_places=2)
    class Meta:
        db_table = 'Resultat'
        managed = True
        verbose_name = 'Resultat'
        verbose_name_plural = 'Resultat'
    
    def __str__(self):
        return f"Résultat pour {self.candidat} à {self.bureau} : {self.nombre_votes} votes au {self.date}"

 


class TotalVotes(models.Model):
    id_total_votes = models.AutoField(primary_key=True)
    candidat = models.OneToOneField(Candidat, on_delete=models.CASCADE)
    nombre_votes = models.IntegerField(default=0)
    pourcentage = models.DecimalField(max_digits=5, decimal_places=2)

    class Meta:
        db_table = 'TotalVotes'
        managed = True
        verbose_name = 'TotalVotes'
        verbose_name_plural = 'TotalVotes'

    def __str__(self):
        return f"{self.candidat} a {self.nombre_votes} votes"



