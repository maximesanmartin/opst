# -*- coding:utf-8 -*-
from opst_plugins.models import *
from django.template.defaultfilters import slugify

class ListeRequete(list):
	def __init__(self):
		list.__init__(self)
		
	def item_exists(self, item):
		return item in self

	def traitement_requete(self, chaine):
		""" Traite le résultat d'une requete sur la table "table"
			sur les attributs "*att"
			à partir de la chaine donnée """
		req = ListeRequete()
		""" POUR UN TAG """
		# On récupère tous les éléments correspondant dans la table
		try:
			req + Tag.objects.filter(slug__startswith=slugify(chaine))
		except KeyError:
			pass
		# Si on obtient des résultats
		if req:
			# On récupère les id ressources associées à la table
			for elem in req:
				# On récupère toutes les id_ressources en rapport ave un id_tag
				for un_tag in elem.items.all():
					try:
						self + Ressource.objects.filter(id=un_tag.id_ressource.id)
					except KeyError:
						pass
		else:
			""" POUR UN AUTEUR """
			# On récupère tous les éléments correspondant dans la table
			try:
				req + Auteur.objects.filter(nom__contains=chaine.capitalize())
			except KeyError:
				pass
			try:
				req + Auteur.objects.filter(prenom__contains=chaine.capitalize())
			except KeyError:
				pass
			# Si on obtient des résultats
			if req:
				# On récupère les id ressources associées à la table
				for elem in req:
					# On récupère toutes les id_ressources en rapport avec un id_tag
					for un_auteur in elem.ressourceauteur_set.all():
						try:
							self + Ressource.objects.filter(id=un_auteur.id_ressource.id)
						except KeyError:
							pass
			else:
				""" POUR UNE REVUE """
				# On récupère tous les éléments correspondant dans la table
				try:
					req + Revue.objects.filter(nom__contains=chaine.capitalize())
				except KeyError:
					pass
				# Si on obtient des résultats
				if req:
					# On récupère les id ressources associées à la table
					for elem in req:
						# On récupère toutes les id_ressources en rapport avec un id_tag
						for une_ressource in elem.ressource_set.all():
							try:
								self + Ressource.objects.filter(id=une_ressource.id)
							except KeyError:
								pass
				else:
					""" POUR UNE SOUS-CATEGORIE """
					# On récupère tous les éléments correspondant dans la table
					try:
						req + SousCategorie.objects.filter(slug__contains=chaine)
					except KeyError:
						pass
					# Si on obtient des résultats
					if req:
						# On récupère les id ressources associées à la table
						for elem in req:
							# On récupère toutes les id_ressources en rapport avec un id_tag
							for une_ressource in elem.ressourcecatsscat_set.all():
								try:
									self + Ressource.objects.filter(id=une_ressource.id_ressource.id)
								except KeyError:
									pass
					else:
						""" POUR UNE CATEGORIE """
						# On récupère tous les éléments correspondant dans la table
						try:
							req + Categorie.objects.filter(slug__contains=chaine)
						except KeyError:
							pass
						# Si on obtient des résultats
						if req:
							# On récupère les id ressources associées à la table
							for elem in req:
								# On récupère toutes les id_ressources en rapport avec un id_tag
								for une_ressource in elem.ressourcecatsscat_set.all():
									try:
										self + Ressource.objects.filter(id=une_ressource.id_ressource.id)
									except KeyError:
										pass
		""" POUR UNE RESSOURCE """
		# On récupère tous les éléments correspondant dans la table
		try:
			self + Ressource.objects.filter(titre__contains=chaine)
		except KeyError:
			pass
		try:
			self + Ressource.objects.filter(slug__contains=slugify(chaine))
		except KeyError:
			pass
		try:
			self + Ressource.objects.filter(texte__contains=chaine)
		except KeyError:
			pass
		try:
			if is_number(chaine):
				self + Ressource.objects.filter(annee=chaine)
		except KeyError:
			pass
		
		return self

	def __add__(self, une_liste):
		""" Ajoute une liste à notre liste """
		for un_item in une_liste:
			if un_item in self:
				raise KeyError()
			self.append(un_item)
		return self
		
	def __str__(self):
		chaine = str("[")
		for i,un_item in enumerate(self):
			chaine += un_item
			if i != len(self) - 1:
				chaine += ", "
		chaine += "]"
		return chaine
#--------- FIN DE LA CLASSE ---------#	
	
def is_number(s):
	try:
		int(s)
		return True
	except ValueError:
		return False