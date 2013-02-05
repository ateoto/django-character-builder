from tastypie.resources import ModelResource, ALL_WITH_RELATIONS
from tastypie import fields
from character_builder.models import (ClassType, Character, Race,
                                        Gender, Alignment, Deity)


class ClassTypeResource(ModelResource):
    class Meta:
        queryset = ClassType.objects.all()
        resource_name = 'class_type'


class RaceResource(ModelResource):
    class Meta:
        queryset = Race.objects.all()
        resource_name = 'race'


class GenderResource(ModelResource):
    class Meta:
        queryset = Gender.objects.all()
        resource_name = 'gender'


class AlignmentResource(ModelResource):
    class Meta:
        queryset = Alignment.objects.all()
        resource_name = 'alignment'


class DeityResource(ModelResource):
    class Meta:
        queryset = Deity.objects.all()
        resource_name = 'deity'


class CharacterResource(ModelResource):
    class_type = fields.ForeignKey(ClassTypeResource, 'class_type', full=True)
    race = fields.ForeignKey(RaceResource, 'race', full=True)
    gender = fields.ForeignKey(GenderResource, 'gender', full=True)
    alignment = fields.ForeignKey(AlignmentResource, 'alignment', full=True)
    deity = fields.ForeignKey(DeityResource, 'deity', full=True)

    class Meta:
        queryset = Character.objects.all()
        resource_name = 'character'
