from .models import *
from django.db.models import Sum
from django.shortcuts import render, redirect,get_object_or_404
from django.contrib.auth.hashers import make_password, check_password
from django.core.exceptions import ValidationError
from .forms import  ElecteurLoginForm

from .models import Candidat 
from django.views import View
from django.contrib import messages



def connexion(request):
    if request.method == 'POST':
        form = ElecteurLoginForm(request.POST)
        if form.is_valid():
            codeEL = form.cleaned_data['code_electeur']
            pwd = form.cleaned_data['mot_de_passe']
            
            electeur = Electeur.objects.filter(code_electeur=codeEL).first()
            try:
                if electeur.actif:
                    if electeur and check_password(pwd, electeur.mot_de_passe) :
               
                        return redirect('candidat_list')  # Redirection correcte
                
                    else:
                        form.add_error(None, 'Code Électeur ou Mot de Passe incorrect')
                else:
                    form.add_error(None, "Votre compte est désactivé parceque vous avez deja réalisé un vote merci de patienter jusqu'a nouvel ordre")
            except Exception as error:
              form.add_error(None, "vous navez pas de compte")
            

    else:
        form = ElecteurLoginForm()

    return render(request, 'login.html', {'form': form})
       
def home (request):
    return render(request, 'accueil.html')


def candidat_list(request ):
    candidats = Candidat.objects.all()
    return render(request, 'candidat_list.html', {'candidats': candidats})





def candidat_detail(request, id):
    candidat = get_object_or_404(Candidat, pk=id)
    
    return render(request, 'candidat_detail.html', {'candidat': candidat})




def vote(request,id):
    if request.method == 'POST':
        form=ElecteurLoginForm(request.POST)
        if form.is_valid():
            codeEL = form.cleaned_data['code_electeur']
            pwd = form.cleaned_data['mot_de_passe']
            
            electeur = Electeur.objects.filter(code_electeur=codeEL).first()
            try:
                bureau= electeur.trouver_bureau_vote()
                if bureau:
                
                    if electeur and check_password(pwd, electeur.mot_de_passe) and electeur.actif:
                        try:
                            vote = Vote(electeur=electeur,   candidat=get_object_or_404(Candidat, pk=id), bureau=BureauDeVote.objects.get(pk=1))
                            vote.save()
                        
                            electeur.actif = False
                            electeur.save()  # Mise à jour du champ actif
                            return redirect('connexion')
                        except Exception as error:
                           form.add_error(None,"vous essayez de voter un candidat qui n'existe plus ou pas")
                    elif electeur.actif==False:
                        form.add_error(None, 'vous etes desormais inactif par consequent vous ne pouvez plus voter ')  
                        return redirect('connexion')
                    else: 

                        form.add_error(None, 'Code Électeur ou Mot de Passe incorrect')   
                
            except Exception as error:
                form.add_error(None, "vous n'appartenez a aucun bureau cela signifi que votre ville ou votre arrondissement n'a pas été correctement enregistré")
                
            
    else:
        form = ElecteurLoginForm()

    return render(request, 'vote.html', {'form': form})


def resultat_total(request):
    resultats = Resultat.objects.values('candidat__nom', 'candidat__prenom', 'bureau__nom', 'nombre_votes', 'pourcentage').order_by('-nombre_votes')

    gagnant = resultats.first() if resultats else None

    return render(request, 'resultat_total.html', {
        'resultats': resultats,
        'gagnant': gagnant
    })




