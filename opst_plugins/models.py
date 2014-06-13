# -*- coding: utf-8 -*-
from django.db import models
from django.template.defaultfilters import slugify
from cms.models import CMSPlugin


class TagCloudPluginModel(CMSPlugin):

    result_page = models.ForeignKey('cms.Page', related_name='opst_plugin_tagcloud')
    items_min = models.PositiveIntegerField(default=3)


class SearchBoxPluginModel(CMSPlugin):

    result_page = models.ForeignKey('cms.Page', related_name='opst_plugin_searchbox')

class NewsFeedEntry(models.Model):

    title            = models.CharField(max_length=128)
    url              = models.URLField()
    publication_date = models.DateTimeField(blank=True, null=True)

    def __unicode__(self): return self.title
	
class NewsFeedPluginModel(CMSPlugin):

    title    = models.CharField(max_length=128)
    list_max = models.PositiveIntegerField(default=8)
    news     = models.ManyToManyField(NewsFeedEntry)


class NewsFeedExtPluginModel(CMSPlugin):

    title    = models.CharField(max_length=128)
    list_max = models.PositiveIntegerField(default=8)
    url      = models.URLField(max_length=1024)


class NewsFeedPagePluginModel(CMSPlugin):

    title       = models.CharField(max_length=128)
    list_max    = models.PositiveIntegerField(default=8)
    url         = models.URLField(max_length=1024)
    update_last = models.DateTimeField(blank=True, null=True)
    pages       = models.ManyToManyField('cms.Page', blank=True, null=True)
    parent_page = models.ForeignKey('cms.Page', blank=True, null=True, related_name='parent_of_newsfeed')

    def update(self):

        import feedparser

        from time import mktime
        from datetime import datetime
        from slugify import slugify

        from django.contrib.sites.models import Site

        from cms.models import Page, Title
        from cms.plugins.text.models import Text

        try: p_last = self.pages.latest('publication_date')
        except Page.DoesNotExist: p_last = None

        try:

            for e in feedparser.parse(self.url)['entries']:

                date  = e.get('published_parsed')
                title = e.get('title')
                body  = e.get('summary')
                url   = e.get('link')

                if date and title and body:

                    date = datetime.fromtimestamp(mktime(date))

                    if p_last and date <= p_last.publication_date: continue

                    p=Page(site=Site.objects.all()[0], in_navigation=False, published=True, template='page-full.html')
                    p.publication_date = date

                    if self.parent_page: p.parent = self.parent_page
            
                    p.save()

                    self.pages.add(p)
                    self.save()

                    t=Title(language='en', title=title, slug='%s-%s' % (slugify(title), p.pk), page=p)
                    t.save()
        
                    pl=p.placeholders.get(slot='page')

                    if url: body = u'%s<p><a href="%s">Lire la suite de l\'article…</a></p>' % (body, url)
                    txt=Text(body=body, language='en', plugin_type='TextPlugin')
                    txt.save()

                    pl.cmsplugin_set.add(txt)
                    pl.save()

        except: pass

        self.update_last = datetime.now()
        self.save()
# This is an auto-generated Django model module.
# You'll have to do the following manually to clean this up:
#     * Rearrange models' order
#     * Make sure each model has one field with primary_key=True
# Feel free to rename the models, but don't rename db_table values or field names.
#
# Also note: You'll have to insert the output of 'django-admin.py sqlcustom [appname]'
# into your database.

class Auteur(models.Model):
    id = models.IntegerField(primary_key=True)
    nom = models.CharField(max_length=90)
    prenom = models.CharField(max_length=90)
    def __unicode__(self):
        return self.nom + ' ' + self.prenom 
    def save(self, *args, **kwargs):
        super(Auteur, self).save(*args, **kwargs) # Call the "real" save() method.
    class Meta:
        db_table = u'auteur'

class Categorie(models.Model):
    id = models.IntegerField(primary_key=True)
    nom = models.CharField(max_length=120)
    slug = models.SlugField(max_length=150)
    def __unicode__(self):
        return self.nom
    class Meta:
        db_table = u'categorie'

class Revue(models.Model):
    id = models.IntegerField(primary_key=True)
    nom = models.CharField(max_length=300)
    nb_num_revues = models.IntegerField(null=True, blank=True, verbose_name="Nombre de numéros de revues")
    def __unicode__(self):
        return self.nom
    class Meta:
        db_table = u'revue'

class Tag(models.Model):
    id = models.IntegerField(primary_key=True)
    nom = models.CharField(max_length=120)
    slug = models.SlugField(max_length=150)
    def __unicode__(self):
        return self.nom
    def nb_tags(self):
        return self.items.count()
    nb_tags.short_description = 'Nombre d\'utilisations du tag'
    class Meta:
        db_table = u'tag'	
	
class Ressource(models.Model):
    id = models.IntegerField(primary_key=True)
    titre = models.CharField(max_length=600)
    slug = models.SlugField(max_length=600, blank=True)
    texte = models.TextField(blank=True)
    lien_texte = models.CharField(max_length=300, blank=True)
    annee = models.IntegerField()
    mois = models.CharField(max_length=30, blank=True)
    lieu = models.CharField(max_length=300, blank=True)
    page_deb = models.IntegerField(null=True, blank=True, verbose_name='Page de début')
    page_fin = models.IntegerField(null=True, blank=True, verbose_name='Page de fin')
    date_debut = models.DateField(null=True, blank=True, verbose_name='Date de début')
    date_fin = models.DateField(null=True, blank=True, verbose_name='Date de fin')
    editeur = models.CharField(max_length=450, blank=True)
    formation = models.CharField(max_length=300, blank=True)
    universite = models.CharField(max_length=300, blank=True, verbose_name='Université')
    discipline = models.CharField(max_length=300, blank=True)
    type_production = models.CharField(max_length=300, blank=True)
    type_rapport = models.CharField(max_length=300, blank=True)
    id_revue = models.ForeignKey(Revue, db_column='id_revue', verbose_name= 'Nom de la revue attribuée', null=True, blank=True)
    tags = models.ManyToManyField(Tag)
    auteurs = models.ManyToManyField(Auteur)
    ordering = ['-annee']
    def __unicode__(self):
        return self.titre
    class Meta:
        db_table = u'ressource'

class SousCategorie(models.Model):
    id = models.IntegerField(primary_key=True)
    nom = models.CharField(max_length=120)
    slug = models.SlugField(max_length=150, blank=True)
    def __unicode__(self):
        return self.nom
    class Meta:
        db_table = u'sous_categorie'

class RessourceCatSsCat(models.Model):
    id = models.IntegerField(primary_key=True)
    id_ressource = models.ForeignKey(Ressource, db_column='id_ressource', verbose_name='Ressource')
    id_categorie = models.ForeignKey(Categorie, db_column='id_categorie', verbose_name='Catégorie')
    id_sous_cat = models.ForeignKey(SousCategorie, db_column='id_sous_cat', verbose_name='Sous-Catégorie')
    def __unicode__(self):
        return u"{} à {}/{}".format(self.id_ressource.titre, self.id_categorie.nom, self.id_sous_cat.nom)
    class Meta:
        db_table = u'ressource_cat_ss_cat'
        verbose_name = 'Ressources - Categories - Sous-Catégorie'

class RessourcePluginModel(CMSPlugin):
    ressource = models.ForeignKey(Ressource, verbose_name='Ressource')
    categorie = models.ForeignKey(Categorie, verbose_name='Catégorie')
    sous_categorie = models.ForeignKey(SousCategorie, verbose_name='Sous-Catégorie')

class MultipleSearchBoxPluginModel(CMSPlugin):
	
    result_page = models.ForeignKey('cms.Page', related_name="opst_plugin_multiplesearchbox")