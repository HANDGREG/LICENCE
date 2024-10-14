from django.contrib import admin

from .models import *
# Register your models here.

class electeur(admin.ModelAdmin):
    list_display=('code_electeur','nom','prenom')






class candidat(admin.ModelAdmin):
    list_display=('code_candidat','nom','prenom','parti')

class bureau (admin.ModelAdmin):
    list_display=('id_bureau','nom','adresse','arrondissement')


class vote (admin.ModelAdmin):
    list_display=('id_vote','electeur','candidat','bureau','date_vote')

    """ def has_delete_permission(self, request, obj=None):
        return False  # Empêche la suppression pour tous les objets

    def has_change_permission(self, request, obj=None):
        return False  # Empêche toute modification"""

class resultat (admin.ModelAdmin):
    list_display=('id_resultat','bureau','candidat','nombre_votes','pourcentage')
class totalvotes (admin.ModelAdmin):
    list_display=('id_total_votes','candidat','nombre_votes','pourcentage')


admin.site.register(Electeur,electeur)

admin.site.register(Candidat,candidat)
admin.site.register(BureauDeVote,bureau)
admin.site.register(Vote,vote)
admin.site.register(Resultat,resultat)
admin.site.register(TotalVotes,totalvotes)
