#-*- coding:utf-8 -*-
from django import forms

class RechercheForm(forms.Form):
	q = forms.CharField(max_length=128)