from tastypie.resources import ModelResource, ALL_WITH_RELATIONS
from tastypie.authentication import SessionAuthentication
from tastypie.authorization import DjangoAuthorization, Authorization
from tastypie import fields
from character_builder.models import (ClassType, Character, Race,
                                        Gender, Alignment, Deity, Source,
                                        Ability, CharacterAbility)


class SourceResource(ModelResource):
    class Meta:
        queryset = Source.objects.all()
        resource_name = 'source'


class ClassTypeResource(ModelResource):
    source = fields.ForeignKey(SourceResource, 'source', full=True)

    class Meta:
        queryset = ClassType.objects.all()
        resource_name = 'class_type'


class RaceResource(ModelResource):
    source = fields.ForeignKey(SourceResource, 'source', full=True)

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


class AbilityResource(ModelResource):
    class Meta:
        queryset = Ability.objects.all()
        resource_name = 'ability'


class CharacterAbilityResource(ModelResource):
    character = fields.ToOneField('character_builder.api.resources.CharacterResource', 'character')
    ability = fields.ForeignKey(AbilityResource, 'ability', full=True)

    class Meta:
        queryset = CharacterAbility.objects.all()
        resource_name = 'CharacterAbility'

    def dehydrate(self, bundle):
        bundle.data['modifier'] = bundle.obj.modifier()
        bundle.data['modifier_half_level'] = bundle.obj.modifier_half_level()

        return bundle


class CharacterResource(ModelResource):
    class_type = fields.ForeignKey(ClassTypeResource, 'class_type', full=True)
    race = fields.ForeignKey(RaceResource, 'race', full=True)
    gender = fields.ForeignKey(GenderResource, 'gender', full=True)
    alignment = fields.ForeignKey(AlignmentResource, 'alignment', full=True)
    deity = fields.ForeignKey(DeityResource, 'deity', full=True)
    abilities = fields.ToManyField(CharacterAbilityResource, 'abilities', full=True)

    class Meta:
        queryset = Character.objects.all()
        resource_name = 'character'

        authentication = SessionAuthentication()
        authorization = Authorization()

    def dehydrate(self, bundle):
        bundle.data['level'] = bundle.obj.current_level().number
        bundle.data['level_xp_needed'] = bundle.obj.current_level().xp_required
        bundle.data['next_level'] = bundle.obj.next_level().number
        bundle.obj.calc_hit_points()
        bundle.data['max_hit_points'] = bundle.obj.max_hit_points
        bundle.data['next_level_xp_needed'] = bundle.obj.next_level().xp_required
        bundle.data['defenses'] = bundle.obj.get_defenses()

        return bundle
