from django.conf.urls import patterns, url, include
#from django.views.generic.base import TemplateView
from tastypie.api import Api
from character_builder.api import ClassTypeResource, CharacterResource

api = Api(api_name='v1')

api.register(ClassTypeResource())
api.register(CharacterResource())

urlpatterns = patterns('',
    #url(r'^$', TemplateView.as_view(template_name = 'character_builder/builder.html')),
    url(r'^$', 'character_builder.views.user_home', name='character-builder-user-home'),
    url(r'^charactersheet/(?P<character_id>\d+)/(?P<character_slug>\w+)/$', 'character_builder.views.sheet', name='character-builder-sheet'),
    url(r'^characterjson/$', 'character_builder.views.character_json', name='character-builder-character-json'),

    url(r'^builder/$', 'character_builder.views.personal', name='character-builder-index'),
    url(r'^builder/personal/$', 'character_builder.views.personal', name='character-builder-personal'),
    url(r'^builder/abilities/(?P<character_id>\d+)/$', 'character_builder.views.abilities', name='character-builder-abilities'),
    url(r'^builder/skills/(?P<character_id>\d+)/$', 'character_builder.views.skills', name='character-builder-skills'),
    url(r'^builder/features/(?P<character_id>\d+)/$', 'character_builder.views.features', name='character-builder-features'),
    url(r'^builder/feats/(?P<character_id>\d+)/$', 'character_builder.views.feats', name='character-builder-feats'),
    url(r'^builder/powers/(?P<character_id>\d+)/$', 'character_builder.views.powers', name='character-builder-powers'),
    url(r'^builder/gear/(?P<character_id>\d+)/$', 'character_builder.views.gear', name='character-builder-gear'),
    url(r'^api/', include(api.urls)),
)
