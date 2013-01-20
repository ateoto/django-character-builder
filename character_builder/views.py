import json

from django.shortcuts import render_to_response, get_object_or_404
from django.http import HttpResponse, Http404
from django.template import loader, RequestContext
from django.contrib.auth.decorators import login_required

from character_builder.models import (Ability, Character, Race,
                                    Source, ClassType, Deity)
from character_builder.forms import CharacterFormUser


@login_required
def user_home(request):
    characters = Character.objects.filter(user=request.user)
    return render_to_response('character_builder/home.html',
            {'characters': characters},
            context_instance=RequestContext(request))


@login_required
def index(request):
    allowed_source = Source.objects.get(name="Player's Handbook")

    races = Race.objects.filter(source=allowed_source)
    classtypes = ClassType.objects.filter(source=allowed_source)
    deities = Deity.objects.all()

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

    t = loader.get_template('character_builder/deity_info.html')
    for deity in deities:
        c = RequestContext(request, {'deity': deity})
        deity.html = t.render(c)

    response_dict['races'] = races
    response_dict['classtypes'] = classtypes
    response_dict['abilities'] = abilities
    response_dict['deities'] = deities
    response_dict['character_form'] = character_form

    return render_to_response('character_builder/builder.html',
            response_dict,
            context_instance=RequestContext(request))


@login_required
def save(request):
    if request.method == "POST":
        response_dict = {}
        character_form = CharacterFormUser(request.POST)
        if character_form.is_valid():
            c = Character()
            c.name = character_form.cleaned_data['name']
            c.user = request.user
            c.race = character_form.cleaned_data['race']
            c.class_type = character_form.cleaned_data['class_type']
            c.alignment = character_form.cleaned_data['alignment']
            c.deity = character_form.cleaned_data['deity']
            c.height = character_form.cleaned_data['height']
            c.weight = character_form.cleaned_data['weight']
            c.age = character_form.cleaned_data['age']
            c.save()

            response_dict['valid'] = True
            response_dict['character_id'] = c.id
        else:
            response_dict['valid'] = False
            response_dict['errors'] = character_form.errors

        return HttpResponse(json.dumps(response_dict), content_type="application/json")
    else:
        raise Http404


@login_required
def save_abilities(request):
    response_dict = {}
    response_dict['valid'] = False
    response_dict['errors'] = request.POST
    return HttpResponse(json.dumps(response_dict), content_type="application/json")


def sheet(request, character_id, character_name):
    c = get_object_or_404(Character, id=character_id, name=character_name)
    return HttpResponse(c.name)
