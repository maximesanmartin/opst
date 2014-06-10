#-*- coding:utf-8 -*-
import operator

CRITERES_POSSIBLES = (
	('TITRE', 'Titre'),
	('TEXTE', 'Texte'),
	('FORMATION', 'Formation'),
	('UNIVERSITE', 'Universite'), 
	('DISCIPLINE', 'Discipline'),
	('TYPE_RAPPORT', 'Type de rapport'),
	('ANNEE', 'Annee de publication'),
	('AUTEUR_NOM', 'Auteur(nom)'),
	('AUTEUR', 'Auteur(nom prenom)'),
	('CATEGORIE', 'Catégorie'),
	('SOUS_CATEGORIE', 'Sous Catégorie'),
	('REVUE', 'Revue'),
	('TAG', 'Tag')
)

COMPARATEURS_POSSIBLES = (
	('CONTIENT', 'contient'),
	('EXACT', 'est exactement'),
	('COMMENCE', 'commence par'),
	('FINIT', 'finit par'),
	('SUP', 'supérieure à'),
	('SUP_EQ', 'supérieure ou égale à'),
	('INF', 'inférieure à'),
	('INF_EQ', 'inférieure ou égale à')
)

OPERATEURS_LOGIQUES = (
	('ET', 'et'),
	('OU', 'ou'),
	('SAUF', 'sauf'),
)

comp = {
	'CONTIENT': '__icontains',
	'EXACT': '__iexact',
	'COMMENCE': '__istartswith',
	'FINIT': '__iendswith',
	'SUP': '__gt',
	'SUP_EQ': '__gte',
	'INF': '__lt',
	'INF_EQ': '__lte'
}

op = {
	'OU': operator.or_,
	'ET': operator.and_,
	'SAUF': operator.and_
}

fields = {
	'TITRE': 'titre',
	'TEXTE': 'texte',
	'AUTEUR_NOM': 'auteurs__nom',
	'CATEGORIE': 'ressource_cat_ss_cat__id_categorie__nom',
	'SOUS_CATEGORIE': 'ressource_cat_ss_cat__id_sous_cat__nom',
	'REVUE': 'id_revue',
	'FORMATION': 'formation',
	'UNIVERSITE': 'universite', 
	'DISCIPLINE': 'discipline',
	'TYPE_RAPPORT': 'type_rapport',
	'ANNEE': 'annee',
	'TAG' : 'tags__nom'
}