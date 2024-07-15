from django import forms
from .models import *


class ElecteurLoginForm(forms.Form):
    code_electeur = forms.CharField(max_length=10, label='Code Électeur',widget=(forms.TextInput(attrs={'class':'code_electeur', 
                                                                                                        'placeholder':"entrez votre code d'electeur"})))
    mot_de_passe = forms.CharField(widget=forms.PasswordInput(attrs={
        'class':'mot_de_passe', 
        'placeholder':"entrez votre mot de passe"
    }), label='Mot de Passe')




