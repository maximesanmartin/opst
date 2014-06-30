import re, copy, datetime

from django.utils.translation import ugettext_lazy as _
from django.conf import settings
from django.utils.safestring import mark_safe
from django.db.models import Count, query

from tagging.models import Tag
from .define import *
from cms.plugin_base import CMSPluginBase
from cms.plugin_pool import plugin_pool
from cms.models.pluginmodel import CMSPlugin as CMSPluginModel
from cms.plugins.inherit.cms_plugins import InheritPagePlaceholderPlugin
#from cms.plugins.inherit.models import InheritPagePlaceholder
from cms.plugins.text.models import Text
from cms.models import Title, Page
from cms.utils import get_language_from_request
from cms.utils.moderator import get_cmsplugin_queryset

from .models import TagCloudPluginModel, SearchBoxPluginModel, NewsFeedPluginModel, RessourcePluginModel, MultipleSearchBoxPluginModel, \
                    NewsFeedExtPluginModel, NewsFeedPagePluginModel, Auteur, Ressource, Tag as Tag1, RessourcePluginModel
from .forms import SearchBoxForm, MultipleSearchBoxForm

from opst_root.define import ListeRequete
from math import log

re_blanks = re.compile('\s+')


class TagCloudPlugin(CMSPluginBase):

    model = TagCloudPluginModel
    name = _("Tag Cloud")
    render_template = "cms_plugins/tagcloud.html"

    def render(self, context, instance, placeholder):

        # q = Tag.objects.extra(
        #     select={'i_count': 'SELECT COUNT(*) FROM tagging_taggeditem WHERE tagging_taggeditem.tag_id = tagging_tag.id',},
        #     where=['i_count > %s' % instance.items_min]
        # ).exclude(name='footer')
        q = Tag1.objects.annotate(i_count=Count('ressource')).filter(i_count__gte=instance.items_min)
		
        context.update({'instance': instance,
                        'tags': map(lambda t: (t, 10 + (min(t.i_count,30) - instance.items_min) * 1), q)})

        return context

plugin_pool.register_plugin(TagCloudPlugin)

# Plugin de recherche simple
class SearchBoxPlugin(CMSPluginBase):

    model = SearchBoxPluginModel
    name = _("Search Box")
    render_template = "cms_plugins/searchbox.html"

    def render(self, context, instance, placeholder):

        f = SearchBoxForm(context['request'].GET)
        f2 = MultipleSearchBoxForm(context['request'].GET)
        # Envoi des variables au template incluant le formulaire f et l'instance de la classe modele
        context.update({'instance': instance,
                        'form2': f2,
                        'form': f,
                        'path': context['request'].path_info,
                        'q': context['request'].GET.get('q')})

        return context

plugin_pool.register_plugin(SearchBoxPlugin)

# Plugin de recherche multi-criteres heritee de CMSPluginBase
class MultipleSearchBoxPlugin(CMSPluginBase):
	
    # Recuperation du modele contenant les champs necessaire a la creation du plugin
    model = MultipleSearchBoxPluginModel
    # Nommage du plugin pour qu'il soit facilement reperable dans la liste des plugins
    name = _("Multiple Search Box")
    # Template ou fichier HTML qui servira de representation visuelle du plugin
    render_template = "cms_plugins/multiplesearchbox.html"

    # Redefinition de la methode render. Cette fonction permet d'envoyer des variables utilisables dans le template
    def render(self, context, instance, placeholder):

        # Instanciation de la classe formulaire et stockage dans la variable f
		# Cette classe contient l'ensemble des champs necessaire a la creation du formulaire de recherche multi-criteres
        f = MultipleSearchBoxForm(context['request'].GET)
        # Envoi des variables au template incluant le formulaire f et l'instance de la classe modele
        context.update({'instance': instance,
                        'form': f})

        return context
# Ajout du plugin a la liste
plugin_pool.register_plugin(MultipleSearchBoxPlugin)

class RessourcePlugin(CMSPluginBase):

    model = RessourcePluginModel
    name = _("Ressource")
    render_template = "cms_plugins/ressource.html"

    def render(self, context, instance, placeholder):

        # Recuperation des auteurs
        print instance.id
        auteurs = Auteur.objects.filter(ressource__id=instance.ressource_id)
        # Recuperation des tags
        tags = Tag1.objects.filter(ressource__id=instance.ressource_id)
        # Donnees de la ressource a passer au template, instance est obligatoire
        context.update({'instance': instance,
                        'tags': tags,
                        'auteurs': auteurs,
                        })

        return context

plugin_pool.register_plugin(RessourcePlugin)

class ListRessourcesPlugin(CMSPluginBase):

    name = _("ListeRessources")
    render_template = "cms_plugins/listressources.html"

    def render(self, context, instance, placeholder):
        ressources = get_ressources(context['request'].path_info)
        # Donnees de la ressource a passer au template, instance est obligatoire
        context.update({'instance': instance,
                        'ressources': ressources,
                        'annees': get_dates(ressources)
                        })

        return context

plugin_pool.register_plugin(ListRessourcesPlugin)

# Plugin de resultat de recherche
class SearchResultPlugin(CMSPluginBase):

    # Utilisation d'un plugin de modeles ordinaire
    model = CMSPluginModel
    # Nommage du plugin
    name = _("Search Result")
    # Template qui servira de representation visuelle du plugin
    render_template = "recherche/recherche.html"

    # Redefinition de la methode ancetre render
    def render(self, context, instance, placeholder):

        if context['request'].GET.get('q'):
            # Recuperation du formulaire rempli avec les donnees
            f = SearchBoxForm(context['request'].GET)
            
            # Si le formulaire est valide(tous les parametres sont remplis, pas de depassement de taille de donnee)
            if f.is_valid():
                
                # Recuperation du parametre q du formulaire
                q = f.cleaned_data.get('q')
		    	# traitement de la chaine envoyee par le formulaire ainsi que des ordres de tri et de la pagination
                (results, nb_res) = traitement_requete_simple(q)
		        # Traitement dans le cas d'envoi de parametre q non renseigne
                try:
                    context.update({'results': results, 'results_n': nb_res, 'query_string': q.strip(), 'sort': context['request'].GET.get('sort')})
                except UnboundLocalError:
                    context.update({'results': [], 'results_n': 0, 'query_string': ''})
        elif context['request'].GET.get('crit_1'):
            (results, nb_res) = traitement_requete_avancee(context)
            context.update({'results': results, 'results_n': nb_res, 'sort': context['request'].GET.get('sort')})
        else:
            context.update({'results': [], 'results_n': 0, 'query_string': ''})
        return context
# Ajout du plugin a la liste
plugin_pool.register_plugin(SearchResultPlugin)

class SiteSearchResultPlugin(CMSPluginBase):

    model = CMSPluginModel
    name = _("Site Search Result")
    render_template = "cms_plugins/searchresult.html"

    def render(self, context, instance, placeholder):

        results = {}

        f = SearchBoxForm(context['request'].GET)

        if f.is_valid():

            q = f.cleaned_data.get('q')
            q_re = '(%s)' % '|'.join(re_blanks.split(q))

            for i in list(Title.objects.filter(title__iregex=q_re)):
                if not i.page in results: results[i.page] = i.title

            for i in list(Text.objects.filter(body__iregex=q_re)):
                if not i.page in results: results[i.page] = i.body
       
        context.update({'results': results, 'results_n': len(results)})

        return context

plugin_pool.register_plugin(SiteSearchResultPlugin)

class SitemapPlugin(CMSPluginBase):

    model = CMSPluginModel
    name = _("Sitemap")
    render_template = "cms_plugins/sitemap.html"

    def render(self, context, instance, placeholder):

        return context

plugin_pool.register_plugin(SitemapPlugin)


class BranchMapPlugin(CMSPluginBase):

    model = CMSPluginModel
    name = _("Branch map")
    render_template = "cms_plugins/branchmap.html"

    def render(self, context, instance, placeholder):

        return context

plugin_pool.register_plugin(BranchMapPlugin)


#class ChildPagesPlugin(CMSPluginBase):

#    model = CMSPluginModel
#    name = _("Child Pages")
#    render_template = "cms_plugins/childpages.html"

#    def render(self, context, instance, placeholder):

#        return context

#plugin_pool.register_plugin(ChildPagesPlugin)


class FocusPlugin(InheritPagePlaceholderPlugin):

    render_template = "cms_plugins/focus.html"
    name = _("Focus")

    def render(self, context, instance, placeholder):

        context = super(FocusPlugin, self).render(context, instance, placeholder)
        context.update({'focus_page': instance.from_page})

        return context

plugin_pool.register_plugin(FocusPlugin)


class NewsFeedPlugin(CMSPluginBase):

    model = NewsFeedPluginModel
    render_template = "cms_plugins/newsfeed.html"
    name = _("News Feed")
    filter_horizontal = ('news',)

    def render(self, context, instance, placeholder):

#        context = super(NewsFeedPluginModel, self).render(context, instance, placeholder)
        context.update({
            'newsfeed': instance.news.filter(
                publication_date__isnull=False)
                .order_by('-publication_date')[0:instance.list_max],
            'instance': instance})

        return context

plugin_pool.register_plugin(NewsFeedPlugin)


class NewsFeedExtPlugin(CMSPluginBase):

    model = NewsFeedExtPluginModel
    render_template = "cms_plugins/newsfeedext.html"
    name = _("News Feed External")
    filter_horizontal = ('news',)

    def render(self, context, instance, placeholder):

        import feedparser

        try: 
            context.update({
                'newsfeed': feedparser.parse(instance.url)['entries'][0:instance.list_max],
                'instance': instance})
        except: pass

        return context

plugin_pool.register_plugin(NewsFeedExtPlugin)


class NewsFeedPagePlugin(CMSPluginBase):

    model = NewsFeedPagePluginModel
    render_template = "cms_plugins/newsfeedext.html"
    name = _("News Feed Page")
    filter_horizontal = ('pages',)

    def render(self, context, instance, placeholder):

        if not instance.update_last or \
            (datetime.datetime.now() - instance.update_last).total_seconds() >= 5*60:
            instance.update()

        context.update({
            'newsfeed': map(lambda e: {'link': e.get_path(), 'title': e.get_title()},
                            instance.pages.all().order_by('-publication_date')[0:instance.list_max]),
            'instance': instance})

        return context

plugin_pool.register_plugin(NewsFeedPagePlugin)


class CarouslideRecentPagesPlugin(CMSPluginBase): #InheritPagePlaceholderPlugin):

#    model = CMSPluginModel
    render_template = "cms_plugins/carouslide.html"
    name = _("Carouslide Recent Pages")

    def render(self, context, instance, placeholder):

        # https://github.com/divio/django-cms/blob/develop/cms/plugins/inherit/cms_plugins.py

        template_vars = {
            'placeholder': placeholder,
        }
        template_vars['object'] = instance
        request = context.get('request', None)
        if context.has_key('request'):
            lang = get_language_from_request(request)
        else:
            lang = settings.LANGUAGE_CODE
        page = instance.placeholder.page
        divs = []

        from_pages = Page.objects.published().exclude(pk=page.pk).order_by('-publication_date')[0:5]

        for from_page in from_pages:

            if page.publisher_is_draft:
                from_page = from_page.get_draft_object()
            else:
                from_page = from_page.get_public_object()

            plugins = get_cmsplugin_queryset(request).filter(
                placeholder__page=from_page,
                language=lang,
                placeholder__slot__iexact='page', #placeholder,
                parent__isnull=True
            ).order_by('position').select_related()
            plugin_output = ['<h1>%s</h1>' % from_page.get_title()]
            template_vars['parent_plugins'] = plugins 
            for plg in plugins:
                tmpctx = copy.copy(context)
                tmpctx.update(template_vars)
                inst, name = plg.get_plugin_instance()
                if inst is None:
                    continue
                outstr = inst.render_plugin(tmpctx, placeholder)
                plugin_output.append(outstr)
            if from_page == from_pages[0]:
                el_attrs = 'class="button carouslide-focus"'
            else:
                el_attrs = 'class="button carouslide-blur"'
            divs.append('<div onclick="document.location=\'%s\'" %s>%s</div>' % \
                (from_page.get_absolute_url(), el_attrs, ''.join(plugin_output)))
#        template_vars['carouslide_content'] = mark_safe('<div>%s</div>' % \
#            '</div><div>'.join(divs))
        template_vars['carouslide_content'] = mark_safe(''.join(divs))
        context.update(template_vars)
        context.update({'instance': instance})
        return context

plugin_pool.register_plugin(CarouslideRecentPagesPlugin)
