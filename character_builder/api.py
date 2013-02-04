from tastypie.resources import ModelResource
from character_builder.models import Character

class CharacterResource(ModelResource):
	class Meta:
		queryset = Character.objects.all()
		resource_name = 'character'
