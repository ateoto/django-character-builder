import logging
log = logging.getLogger(__name__)
import json
import math

from django.shortcuts import render_to_response, get_object_or_404
from django.http import HttpResponse, Http404, HttpResponseRedirect
from django.core.urlresolvers import reverse
from django.template import loader, RequestContext
from django.contrib.auth.decorators import login_required

from character_builder.models import (Ability, Character, Race,
                                    Source, ClassType, Deity,
                                    CharacterAbility, Skill, CharacterSkill,
                                    ClassFeature, RaceFeature, Level)
from character_builder.forms import (CharacterFormUser, CharacterAbilityForm,
                                    CharacterGetterForm)


@login_required
def user_home(request):
    response_dict = {}
    response_dict['user'] = request.user
    response_dict['characters'] = Character.objects.filter(user=request.user)
    return render_to_response('character_builder/home.html',
            response_dict,
            context_instance=RequestContext(request))


@login_required
def personal(request):
    if request.method == "POST":
        character_form = CharacterFormUser(request.POST)
        if character_form.is_valid():
            c = Character()
            c.name = character_form.cleaned_data['name']
            c.user = request.user
            c.race = character_form.cleaned_data['race']
            c.gender = character_form.cleaned_data['gender']
            c.class_type = character_form.cleaned_data['class_type']
            c.alignment = character_form.cleaned_data['alignment']
            c.deity = character_form.cleaned_data['deity']
            c.height = character_form.cleaned_data['height']
            c.weight = character_form.cleaned_data['weight']
            c.age = character_form.cleaned_data['age']
            c.save()

            return HttpResponseRedirect(reverse('character-builder-abilities', kwargs={'character_id': c.id}))
    else:
        character_form = CharacterFormUser()

    allowed_source = Source.objects.get(name="Player's Handbook")

    races = Race.objects.filter(source=allowed_source)
    classtypes = ClassType.objects.filter(source=allowed_source)
    deities = Deity.objects.all()

    abilities = Ability.objects.all()

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

    response_dict['user'] = request.user
    response_dict['races'] = races
    response_dict['classtypes'] = classtypes
    response_dict['abilities'] = abilities
    response_dict['deities'] = deities
    response_dict['character_form'] = character_form

    return render_to_response('character_builder/personal.html',
            response_dict,
            context_instance=RequestContext(request))


@login_required
def abilities(request, character_id):
    character = Character.objects.get(id=character_id)

    if request.method == 'POST':
        abilities_form = CharacterAbilityForm(request.POST)
        if abilities_form.is_valid():
            for ability in Ability.objects.all():
                value = abilities_form.cleaned_data[ability.name.lower()]
                ca, created = CharacterAbility.objects.get_or_create(character=character,
                                                                    ability=ability,
                                                                    defaults={'value': value})
                ca.value = value
                ca.save()

            return HttpResponseRedirect(reverse('character-builder-skills', kwargs={'character_id': character.id}))

    else:
        abilities_form = CharacterAbilityForm()

    response_dict = {}
    response_dict['abilities_form'] = abilities_form
    response_dict['abilities'] = Ability.objects.all()
    response_dict['character'] = character

    return render_to_response('character_builder/abilities.html',
            response_dict,
            context_instance=RequestContext(request))


@login_required
def skills(request, character_id):
    character = Character.objects.get(id=character_id)
    if request.method == 'POST':
        trained_skills_ids = request.POST.getlist('skills')
        trained_skills = []

        if character.race == Race.objects.get(name="Eladrin"):
            trained_skills.append(Skill.objects.get(id=request.POST.get('eladrin_bonus')))

        for skill_id in trained_skills_ids:
            trained_skills.append(Skill.objects.get(id=skill_id))

        for skill in Skill.objects.all():
            if skill in trained_skills:
                trained = True
                trained_mod = 5
            else:
                log.debug("%s is not trained" % (skill.name))
                trained = False
                trained_mod = 0

            # Do we get a Race bonus?
            race_modifier = 0

            race_skill_mod_qs = character.race.skill_mods.filter(skill=skill)
            if race_skill_mod_qs.exists():
                race_skill_mod = race_skill_mod_qs.get()
                race_modifier = race_skill_mod.modifier

            cs = CharacterSkill(character=character, skill=skill, is_trained=trained)
            ca = character.abilities.get(ability=skill.ability)
            modifier = int(math.floor((math.fabs(ca.value) - 10) / 2))
            cs.value = modifier + trained_mod + race_modifier + int(math.floor(character.level / 2))
            log.debug("%s : %s" % (skill.name, cs.value))
            cs.save()

        return HttpResponseRedirect(reverse('character-builder-features', kwargs={'character_id': character.id}))

    response_dict = {}
    response_dict['character'] = character
    response_dict['skills'] = Skill.objects.all()

    return render_to_response('character_builder/skills.html',
            response_dict,
            context_instance=RequestContext(request))


@login_required
def features(request, character_id):
    response_dict = {}
    character = Character.objects.get(id=character_id)

    if request.method == "POST":
        return HttpResponse('Critical Miss.')

    response_dict['character'] = character

    class_features = ClassFeature.objects.filter(class_type=character.class_type)
    race_features = RaceFeature.objects.filter(race=character.race)

    response_dict['class_features'] = class_features.filter(requires_choice=False)
    response_dict['race_features'] = race_features.filter(requires_choice=False)
    response_dict['class_features_choice'] = class_features.filter(requires_choice=True)
    response_dict['race_features_choice'] = class_features.filter(requires_choice=True)

    return render_to_response('character_builder/features.html',
            response_dict,
            context_instance=RequestContext(request))


@login_required
def feats(request, character_id):
    return HttpResponse('Word')


@login_required
def powers(request, character_id):
    pass


@login_required
def gear(request, character_id):
    pass


def sheet(request, character_id, character_slug):
    c = get_object_or_404(Character, id=character_id, slug_name=character_slug)
    response_dict = {}
    response_dict['character'] = c

    response_dict['character_getter_form'] = CharacterGetterForm({'character': c.id})

    return render_to_response('character_builder/sheet.html',
        response_dict,
        context_instance=RequestContext(request))


def character_json(request):
    if request.method == "POST":
        response_dict = {}
        getter_form = CharacterGetterForm(request.POST)
        if getter_form.is_valid():
            character = Character.objects.get(id=getter_form.cleaned_data['character'])
            level = Level.objects.order_by('-xp_required').filter(xp_required__lte=character.xp)[:1].get()
            try:
                next_level_xp_required = Level.objects.get(number=level.number + 1).xp_required
            except:
                next_level_xp_required = 0

            response_dict['character'] = {
                'character_id': character.id,
                'name': character.name,
                'level': level.number,
                'xp': character.xp,
                'next_level_xp_required': next_level_xp_required,
                'hp': character.hit_points,
                'race_id': character.race.id,
                'race_name': character.race.name,
                'class_type_id': character.class_type.id,
                'class_type_name': character.class_type.name}
        else:
            response_dict['errors'] = getter_form.errors

        return HttpResponse(json.dumps(response_dict), content_type="application/json")
    else:
        raise Http404
