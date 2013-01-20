from django.conf.urls import patterns, url
#from django.views.generic.base import TemplateView

urlpatterns = patterns('',
    #url(r'^$', TemplateView.as_view(template_name = 'character_builder/builder.html')),
    url(r'^$', 'character_builder.views.user_home', name='character-builder-user-home'),
    url(r'^builder/$', 'character_builder.views.index', name='character-builder-index'),
    url(r'^builder/save/$', 'character_builder.views.save', name='character-builder-save'),
    url(r'^charactersheet/(?P<character_id>\d+)/(?P<character_name>\w+)/$', 'character_builder.views.sheet', name='character-builder-sheet'),
)
