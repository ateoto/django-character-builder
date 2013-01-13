from django.shortcuts import render_to_response
from django.http import HttpResponse

from character_builder.models import Character

def index(request):
    return render_to_response('character_builder/builder.html',{})
