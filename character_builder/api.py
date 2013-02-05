from tastypie.resources import ModelResource, ALL_WITH_RELATIONS
from tastypie import fields
from character_builder.models import ClassType, Character


class ClassTypeResource(ModelResource):
    class Meta:
        queryset = ClassType.objects.all()
        resource_name = 'class_type'


class CharacterResource(ModelResource):
    class_type = fields.ForeignKey(ClassTypeResource, 'class_type', full=True)

    class Meta:
        queryset = Character.objects.all()
        resource_name = 'character'
        filtering = {
            'class_type': ALL_WITH_RELATIONS,
        }
