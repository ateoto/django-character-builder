from django.shortcuts import render_to_response
from django.http import HttpResponse
from django.template import Context, loader, RequestContext

from character_builder.models import Character, Race, Source, ClassType
from character_builder.forms import CharacterFormStepOne


def index(request):
    form = CharacterFormStepOne()

    allowed_source = Source.objects.get(name="Player's Handbook")

    races = Race.objects.filter(source=allowed_source)
    classtypes = ClassType.objects.filter(source=allowed_source)

    response_dict = {}

    t = loader.get_template('character_builder/race_info.html')
    for race in races:
        c = Context({'race': race})
        race.html = t.render(c)

    t = loader.get_template('character_builder/classtype_info.html')
    for classtype in classtypes:
        c = Context({'classtype': classtype})
        classtypes.html = t.render(c)

    response_dict['races'] = races
    response_dict['classtypes'] = classtypes
    response_dict['form'] = form
    return render_to_response('character_builder/builder.html',
            response_dict,
            context_instance=RequestContext(request))


def build_one(request):
    pass


def step_one(request):
    if request.method == 'POST':
        form = CharacterFormStepOne(request.POST)
        if form.is_valid():
            return HttpResponse('Rock and Roll')
    else:
        form = CharacterFormStepOne()

        return render_to_response('character_builder/builder.html',
                {'form': form},
                context_instance=RequestContext(request))
