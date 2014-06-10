# -*- coding:utf-8 -*-
from django import forms
from .data import *

# Formulaire de recherche simple heritant de la classe Form du module forms
class SearchBoxForm(forms.Form):
	# On instancie un champs chaine de caracteres dans la variable q
    q = forms.CharField(max_length=128)
	
# Formulaire de recherche multi-critere contenant 4 criteres
class MultipleSearchBoxForm(forms.Form):
	crit_1 = forms.ChoiceField(choices=CRITERES_POSSIBLES)
	comp_1 = forms.ChoiceField(choices=COMPARATEURS_POSSIBLES)
	query_1 = forms.CharField(max_length=128)
	op_1 = forms.ChoiceField(choices=OPERATEURS_LOGIQUES)
	crit_2 = forms.ChoiceField(choices=CRITERES_POSSIBLES)
	comp_2 = forms.ChoiceField(choices=COMPARATEURS_POSSIBLES)
	query_2 = forms.CharField(max_length=128)
	op_2 = forms.ChoiceField(choices=OPERATEURS_LOGIQUES)
	crit_3 = forms.ChoiceField(choices=CRITERES_POSSIBLES)
	comp_3 = forms.ChoiceField(choices=COMPARATEURS_POSSIBLES)
	query_3 = forms.CharField(max_length=128)
	op_3 = forms.ChoiceField(choices=OPERATEURS_LOGIQUES)
	crit_4 = forms.ChoiceField(choices=CRITERES_POSSIBLES)
	comp_4 = forms.ChoiceField(choices=COMPARATEURS_POSSIBLES)
	query_4 = forms.CharField(max_length=128)