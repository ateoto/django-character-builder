from django.shortcuts import render_to_response
from django.http import HttpResponse
from django.template import Context, loader, RequestContext
from django.contrib.auth.decorators import login_required

from character_builder.models import Ability, Character, Race, Source, ClassType
from character_builder.forms import CharacterFormUser


@login_required
def user_home(request):
    characters = Character.objects.filter(user=request.user)
    return render_to_response('character_builder/home.html',
            {'characters': characters},
            context_instance=RequestContext(request))


def index(request):
    allowed_source = Source.objects.get(name="Player's Handbook")

    races = Race.objects.filter(source=allowed_source)
    classtypes = ClassType.objects.filter(source=allowed_source)
    abilities = Ability.objects.all()

    character_form = CharacterFormUser()
    character_form.fields['race'].queryset = races
    character_form.fields['class_type'].queryset = classtypes

    response_dict = {}

    t = loader.get_template('character_builder/race_info.html')
    for race in races:
        c = RequestContext(request, {'race': race})
        race.html = t.render(c)

    t = loader.get_template('character_builder/classtype_info.html')
    for classtype in classtypes:
        c = RequestContext(request, {'classtype': classtype})
        classtype.html = t.render(c)

    response_dict['races'] = races
    response_dict['classtypes'] = classtypes
    response_dict['abilities'] = abilities
    response_dict['character_form'] = character_form
    return render_to_response('character_builder/builder.html',
            response_dict,
            context_instance=RequestContext(request))
