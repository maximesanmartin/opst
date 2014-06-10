#-*- coding:utf-8 -*-

""" Ce fichier permet de gerer l'interface
	graphique de l'administration des modeles de donnee
	crees dans le fichier models.py """

from django.contrib import admin
from .models import *

# Le modele "NewsFeedEntry" est ajoute a l'interface d'admnistration
admin.site.register(NewsFeedEntry)

# Cette classe permet d'afficher plusieurs formulaires de ressources dans la classe qui l'appelera  
class RessourceInline(admin.StackedInline):
	# Modele a afficher
    model = Ressource
	# Nombre de formulaire a envoyer
    extra = 3

# Cette classe gere l'affichage d'un tag
class TagInline(admin.TabularInline):
    model = Ressource.tags.through
    verbose_name = u"Tag"
    verbose_name_plural = u"Tags"

# Idem que "TagInline" mais pour "Auteur"
class AuteurInline(admin.StackedInline):
    model = Ressource.auteurs.through
    verbose_name = u"Auteur"
    verbose_name_plural = u"Auteurs"

# Cette classe gere l'affichage du modele Ressource
class RessourceAdmin(admin.ModelAdmin):
    # Configuration de la liste
    list_display = ('titre', 'slug', 'annee')
	# list_filter filtre les resultats de recherche en fonction des valeurs données dans le tuple
    list_filter = ('annee', 'mois')
	# search_fields filtre les resultats de la recherche en fonction des valeurs données dans le tuple
    search_fields = ('titre', 'texte')
	# Trie par défaut par "id"
    ordering = ('id', )
    # Configuration du formulaire d'édition
    fieldsets = (
        # Fieldset 1 : meta-info (titre, auteur…)
       ('Informations Générales', {
            'fields': ('titre', 'slug', 'annee', 'mois', 'lieu', 'editeur', 'formation', 'universite', 'discipline')
        }),
        # Fieldset 2 : contenu de la ressource
        ('Contenu de la ressource', {
           'fields': ('texte', 'lien_texte', 'page_deb', 'page_fin', 'date_debut', 'date_fin', 'type_production', 'type_rapport')
        }),
		# Fieldset 3 : revue
        ('Revue', {
           'description': u'Choisissez une revue en rapport avec votre ressource',
           'fields': ('id_revue', )
        }),
    )
	# Remplie automatiquement le champ "slug" avec "titre"
    prepopulated_fields = {'slug': ('titre', ), }
    exclude = ("tags", )
    inlines = (
       TagInline, AuteurInline
    )
	
class RessourceCatSsCatAdmin(admin.ModelAdmin):
    list_display = ('id_ressource', 'id_categorie', 'id_sous_cat')
    search_fields = ('id_ressource__titre', 'id_ressource__texte', 'id_categorie__nom', 'id_sous_cat__nom')
    fieldsets = (
        # Fieldset 1 : meta-info (titre, auteur…)
       ('', {
            'fields': ('id_ressource', 'id_categorie', 'id_sous_cat')
        }),
    )
		
# Cette classe gere l'affichage du modele Auteur
class AuteurAdmin(admin.ModelAdmin):
    list_display = ('id', 'nom')
    fieldsets = (
        # Fieldset 1 : meta-info (titre, auteur…)
       ('Auteur', {
            'fields': ('nom', 'prenom')
        }),
	)
	
# Cette classe gere l'affichage du modele Tag
class TagAdmin(admin.ModelAdmin):
    list_display = ('id', 'nom')
    fieldsets = (
        # Fieldset 1 : meta-info (titre, auteur…)
       ('Tag', {
            'fields': ('nom', )
        }),
	)
	
# Cette classe gere l'affichage du modele Revue
class RevueAdmin(admin.ModelAdmin):
    list_display = ('id', 'nom')
    fieldsets = (
        # Fieldset 1 : meta-info (titre, auteur…)
       ('Revue', {
            'fields': ('nom', 'nb_num_revues')
        }),
	)

# Cette classe gere l'affichage du modele Categorie
class CategorieAdmin(admin.ModelAdmin):
    list_display = ('id', 'nom')
    fieldsets = (
        # Fieldset 1 : meta-info (titre, auteur…)
       ('Categorie', {
            'fields': ('nom', 'slug')
        }),
	)
    prepopulated_fields = {'slug': ('nom', ), }

# Cette classe gere l'affichage du modele SousCategorie
class SousCategorieAdmin(admin.ModelAdmin):
    list_display = ('id', 'nom')
    fieldsets = (
        # Fieldset 1 : meta-info (titre, auteur…)
       ('Sous-Categorie', {
            'fields': ('nom', 'slug')
        }),
	)
    prepopulated_fields = {'slug': ('nom', ), }

# Ajout d'autres modeles
admin.site.register(Ressource, RessourceAdmin)
admin.site.register(RessourceCatSsCat, RessourceCatSsCatAdmin)
admin.site.register(Categorie, CategorieAdmin)
admin.site.register(SousCategorie, SousCategorieAdmin)
admin.site.register(Revue, RevueAdmin)
admin.site.register(Tag, TagAdmin)
admin.site.register(Auteur, AuteurAdmin)