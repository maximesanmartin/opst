# Create your views here.
# -*- coding:utf-8 -*-
from django.http import HttpResponseRedirect, HttpResponse
from opst_plugins.models import Ressource, Categorie
from django.template import *
from django.shortcuts import render
from django.utils import timezone
from define import *

def affichage_ressource(request, slug):
	""" Affiche une ressource complete comprenant
		les tags, les auteurs, les categories """
	edit = request.GET.get('edit')
	# Récupération de la ressource
	ressource = Ressource.objects.get(slug=slug)
	# Récupération de la revue
	try:
		revue = Revue.objects.get(id=ressource.id_revue.id)
	except AttributeError:
		pass
	# Récupération des auteurs
	auteurs = ressource.auteurs.all()
	# Récupération des tags
	tags = ressource.tags.all()
	# Récupération des cats
	cats_ss_cats = Categorie.objects.filter(ressourcecatsscat__id_ressource=ressource.id)
	return render(request, 'recherche/affichage_page.html', locals())