#-*- coding:utf-8 -*-
from django.db.models import Q
from .models import Ressource
from .data import *

def traitement_requete_simple(query):
	""" Cette fonction traite la chaine query donne
		en parametre et renvoie une liste
		de ressources correspondantes """
	# On regroupe tous les mots separes par des espaces dans une liste
	liste = query.split()
	# Si la liste n'est pas vide on la rempli avec toutes les ressources qui existent 
	if liste:
		req = Ressource.objects.all()
	else:
		req = []
	# la liste va etre filtree a chaque iteration et va conserver les ressources en rapport avec les chaines donnees
	for chaine in liste:
		req = req.filter(Q(id_revue__nom__icontains=chaine) \
				| Q(tags__nom__iexact=chaine) \
				| Q(auteurs__nom__iexact=chaine) \
				| Q(auteurs__prenom__iexact=chaine) \
				| Q(ressourcecatsscat__id_categorie__nom__iexact=chaine) \
				| Q(ressourcecatsscat__id_sous_cat__nom__icontains=chaine) \
				| Q(titre__icontains=chaine) \
				| Q(texte__icontains=chaine) \
				| Q(formation__icontains=chaine) \
				| Q(universite__icontains=chaine) \
				| Q(discipline__icontains=chaine) \
				| Q(type_rapport__icontains=chaine) \
				| Q(annee__iexact=chaine) \
				| Q(mois__iexact=chaine)).distinct().order_by('-annee')
	# On recupere le total de resultats pour un affichage ulterieur
	nb_res = len(req)
	# On renvoie un tuple contenant l'ensemble des ressources d'une page donnee et le total des resultats
	return (req, nb_res)
		
def traitement_requete_avancee(context):
	""" Permet de realiser une recherche multicriteres a
		partir des parametres de l'url contenues dans context """
	# On appelle la fonction requete a partir des parametre des champ du formulaire
	argument_1 = requete(context['request'].GET.get('query_1'), context['request'].GET.get('comp_1'), context['request'].GET.get('crit_1'))
	argument_2 = requete(context['request'].GET.get('query_2'), context['request'].GET.get('comp_2'), context['request'].GET.get('crit_2'), context['request'].GET.get('op_1'))
	argument_3 = requete(context['request'].GET.get('query_3'), context['request'].GET.get('comp_3'), context['request'].GET.get('crit_3'), context['request'].GET.get('op_2'))
	argument_4 = requete(context['request'].GET.get('query_4'), context['request'].GET.get('comp_4'), context['request'].GET.get('crit_4'), context['request'].GET.get('op_3'))
	# On filtre le contenu du modele Ressource selon les arguments definis au-dessus et on trie par defaut par annees
	req = Ressource.objects.filter(reduce(op[context['request'].GET.get('op_3')], \
								[reduce(op[context['request'].GET.get('op_2')], \
								[reduce(op[context['request'].GET.get('op_1')], \
								[argument_1, argument_2]), argument_3]), argument_4])).distinct().order_by('-annee')
	# On recupere le nombre de resultats
	nb_res = len(req)
	# On renvoie un tuple avec les resultats et le nombre
	return (req, nb_res)
	
def requete(query, compar, field, oper=''):
	""" Cette fonction effectue une requete sur un champ renseigne field
		qui est compare au mot-clé query a partir du comparateur compar """
	# Si le champ passe en parametre est Auteur nom et prenom
	if field == 'AUTEUR':
		# On range les mots-cles dans une liste
		liste = query.split()
		try:
			ch_1 = liste.pop()
			ch_2 = liste.pop()
			# Si l'operateur logique est SAUF
			if oper == 'SAUF':
				# On enleve les resultats de cette requete au resultat final
				return ~Q(Q(**{'auteurs__nom'+comp[compar]: ch_1}) & Q(**{'auteurs__prenom'+comp[compar]: ch_2}) | Q(**{'auteurs__nom'+comp[compar]: ch_2}) & Q(**{'auteurs__prenom'+comp[compar]: ch_1}))
			else:
				# Sinon on recupere les resultats
				return Q(Q(**{'auteurs__nom'+comp[compar]: ch_1}) & Q(**{'auteurs__prenom'+comp[compar]: ch_2}) | Q(**{'auteurs__nom'+comp[compar]: ch_2}) & Q(**{'auteurs__prenom'+comp[compar]: ch_1}))
		# Dans le cas ou il n'y a aucun ou qu'un mot-cle donne
		except IndexError:
			# Si l'operateur logique est SAUF
			if oper == 'SAUF':
				# On enleve les resultats de cette requete au resultat final
				return(~Q(**{'auteurs__nom'+comp[compar]: query}))
			else:
				# Sinon on recupere les resultats
				return(Q(**{'auteurs__nom'+comp[compar]: query}))
	# Dans les autres cas ou le champ n'est pas AUTEUR
	# Si l'operateur logique est SAUF
	if oper == "SAUF":
		# On enleve les resultats de cette requete au resultat final
		return ~Q(**{fields[field]+comp[compar]: query})
	else:
		# Sinon on recupere les resultats
		return Q(**{fields[field]+comp[compar]: query})
		
def get_ressources(path):
	""" Cette fonction permet de récupérer l'ensemble des ressources
		d'une sous-catégorie d'une catégorie à partir de l'url path donnée """
	path = path.strip('/')
	(cat,sous_cat) = path.split('/')
	return Ressource.objects.filter(ressourcecatsscat__id_categorie__slug__iexact=cat, ressourcecatsscat__id_sous_cat__slug__iexact=sous_cat).order_by('-annee')
	
def get_dates(ressources):
	list = []
	for res in ressources:
		if res.annee not in list:
			list.append(res.annee)
	list.sort(key=int)
	return list
	
	