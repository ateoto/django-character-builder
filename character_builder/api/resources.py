from tastypie.resources import ModelResource, ALL_WITH_RELATIONS
from tastypie import fields
from tastypie.authentication import SessionAuthentication, Authentication
from tastypie.authorization import DjangoAuthorization, Authorization
from character_builder.models import (ClassType, Character, Race,
                                        Gender, Alignment, Deity, Source,
                                        Ability, CharacterAbility, Power)


class MySessionAuthentication(SessionAuthentication):
    '''
    Authenticates everyone if the request is GET otherwise performs
    SessionAuthentication.
    '''

    def is_authenticated(self, request, **kwargs):
        if request.method == 'GET':
            return True
        return super(MySessionAuthentication, self).is_authenticated(request, **kwargs)


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

    class Meta:
        queryset = Character.objects.all()
        resource_name = 'character'
        authentication = MySessionAuthentication()
        authorization = DjangoAuthorization()

    def dehydrate(self, bundle):
        bundle.data['level'] = bundle.obj.current_level().number
        bundle.data['level_xp_needed'] = bundle.obj.current_level().xp_required
        bundle.data['next_level'] = bundle.obj.next_level().number
        bundle.data['next_level_percentage'] = bundle.obj.next_level_percentage()
        bundle.obj.calc_hit_points()
        bundle.data['max_hit_points'] = bundle.obj.max_hit_points
        bundle.data['hp_percentage'] = bundle.obj.hp_percentage()
        bundle.data['next_level_xp_needed'] = bundle.obj.next_level().xp_required
        bundle.data['abilities'] = bundle.obj.get_abilities()
        bundle.data['defenses'] = bundle.obj.get_defenses()
        bundle.data['powers'] = bundle.obj.get_powers()

        return bundle


class CharacterHealthResource(ModelResource):
    class Meta:
        queryset = Character.objects.all()
        resource_name = 'character_health'
        fields = ['hit_points', 'max_hit_points']


class PowerResource(ModelResource):
    class Meta:
        queryset = Power.objects.all().select_subclasses()
        resource_name = 'power'

    def dehydrate(self, bundle):
        bundle.data['power_type'] = bundle.obj.power_type.name
        bundle.data['action_type'] = bundle.obj.action_type.name
        bundle.data['range_type'] = bundle.obj.range_type.name
        bundle.data['keywords'] = [keyword.name for keyword in bundle.obj.keywords.all()]
        bundle.data['usage'] = bundle.obj.usage.name
        bundle.data['line_detail'] = bundle.obj.line_detail()

        if bundle.obj.hit_modifier is not None:
            bundle.data['hit_modifier_abbreviation'] = bundle.obj.hit_modifier.abbreviation.lower()
        if bundle.obj.secondary_hit_modifier is not None:
            bundle.data['secondary_hit_modifier_abbreviation'] = bundle.obj.secondary_hit_modifier.abbreviation.lower()
        if bundle.obj.sustain_action is not None:
            bundle.data['sustain_action'] = bundle.obj.sustain_action.name

        if hasattr(bundle.obj, 'class_type'):
            bundle.data['class_type'] = bundle.obj.class_type.name
        if hasattr(bundle.obj, 'race'):
            bundle.data['race'] = bundle.obj.race.name
        if hasattr(bundle.obj, 'feat'):
            bundle.data['class_type'] = bundle.obj.feat.name

        return bundle
