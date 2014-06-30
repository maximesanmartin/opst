# Create your views here.
# -*- coding:utf-8 -*-
from django.http import HttpResponseRedirect, HttpResponse
from opst_plugins.models import *
from django.template import *
from django.shortcuts import render, get_object_or_404
from django.http import Http404
from django.core.urlresolvers import reverse
import json
import datetime
from django.utils import timezone
from form import RechercheForm
from define import *

def get_ressources(request):
    if request.is_ajax():
        q = request.GET.get('term', '')
        res = Ressource.objects.filter(titre__icontains = q )[:20]
        results = []
        for ressource in res:
            ressource_json = {}
            ressource_json['id'] = ressource.id
            ressource_json['label'] = ressource.titre
            ressource_json['value'] = ressource.titre
            results.append(ressource_json)
        data = json.dumps(results)
    else:
        data = 'fail'
    mimetype = 'application/json'
    return HttpResponse(data, mimetype)

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

def search(request):
	if request.method == 'GET':
		form = RechercheForm(request.GET)
		if form.is_valid():
			url = 'recherche/recherche.html'
			q = form.cleaned_data['q']
			list_q = q.split()
			res = ListeRequete()
			for une_chaine in list_q:
				res.traitement_requete(une_chaine)
				taille = len(res)
				res.sort()
		else:
			url = 'recherche/accueil.html'
			res = []
			q = ''
	else:
		form = RechercheForm()
		url = 'recherche/accueil.html'
		res = []
		q = ''
	return render(request, url, {'results': res, 'results_n': len(res), 'query_string': q})