from django.db import models

from model_utils.managers import InheritanceManager
from .attributes import (Ability, Skill, Modifier)
from .characteristics import (Deity)
from .races import (Race, RaceFeature, RaceFeatureChoice)
from .classtypes import (ClassType, ClassFeature, ClassFeatureChoice)
from .items import (ArmorType)


class FeatManager(models.Manager):
    def get_eligible(self, character):
        qs = super(FeatManager, self).get_query_set()
        for feat in qs:
            if not feat.character_eligible(character):
                qs = qs.exclude(id=feat.id)

        return qs

class FeatChoice(models.Model):
    name = models.CharField(max_length=50)
    benefit = models.TextField()

    class Meta:
        app_label = 'character_builder'


class Feat(models.Model):
    name = models.CharField(max_length=50)
    benefit = models.TextField()
    special = models.TextField(blank=True)
    has_passive_effects = models.BooleanField(default=False)
    passive_effects = models.ManyToManyField(Modifier, blank=True)
    can_retake = models.BooleanField(default=False)
    requires_choice = models.BooleanField(default=False)
    choices = models.ManyToManyField(FeatChoice, blank=True)
    objects = FeatManager()

    class Meta:
        app_label = 'character_builder'

    def __unicode__(self):
        return self.name

    def character_eligible(self, character):
        eligible = []
        for prereq in FeatPrereq.objects.filter(feat=self).select_subclasses():
            eligible.append(prereq.character_eligible(character))

        return all(eligible)


class FeatPrereq(models.Model):
    feat = models.ForeignKey(Feat, related_name='prereqs')
    objects = InheritanceManager()

    class Meta:
        app_label = 'character_builder'


class FeatRacePrereq(FeatPrereq):
    race = models.ForeignKey(Race)

    class Meta:
        app_label = 'character_builder'

    def __unicode__(self):
        return '%s requires %s' % (self.feat.name, self.race.name)
    
    def character_eligible(self, character):
        return self.race == character.race


class FeatClassTypePrereq(FeatPrereq):
    class_type = models.ForeignKey(ClassType)

    class Meta:
        app_label = 'character_builder'

    def __unicode__(self):
        return '%s requires %s' % (self.feat.name, self.class_type.name)

    def character_eligible(self, character):
        return self.class_type == character.class_type


class FeatClassFeaturePrereq(FeatPrereq):
    classfeature = models.ForeignKey(ClassFeature)

    class Meta:
        app_label = 'character_builder'

    def __unicode__(self):
        return '%s requires %s' % (self.feat.name, self.classfeature.name)

    def character_eligible(self, character):
            return character.class_features.filter(class_feature=self.classfeature).exists()


class FeatAbilityPrereq(FeatPrereq):
    ability = models.ForeignKey(Ability)
    value = models.IntegerField()

    class Meta:
        app_label = 'character_builder'

    def __unicode__(self):
        return '%s requires %s %i' % (self.feat.name, self.ability.name, self.value)

    def character_eligible(self, character):
        ca = CharacterAbility.objects.get(ability=self.ability, character=character)
        return ca.value >= self.value


class FeatSkillPrereq(FeatPrereq):
    skill = models.ForeignKey(Skill)

    class Meta:
        app_label = 'character_builder'

    def character_eligible(self, character):
        return CharacterSkill.objects.filter(skill=self.skill, character=character, is_trained=True).exists()


class FeatSkillOrSkillPrereq(FeatPrereq):
    allowed_skills = models.ManyToManyField(Skill)

    class Meta:
        app_label = 'character_builder'

    def character_eligible(self, character):
        return CharacterSkill.objects.filter(skill__in=self.allowed_skills.all(), character=character, is_trained=True).exists()


class FeatFeatPrereq(FeatPrereq):
    pre_feat = models.ForeignKey(Feat)

    class Meta:
        app_label = 'character_builder'

    def character_eligible(self, character):
        CharacterFeat.objects.get(feat=self.pre_feat, character=character).exists()


class FeatDeityPrereq(FeatPrereq):
    deity = models.ForeignKey(Deity)

    class Meta:
        app_label = 'character_builder'

    def __unicode__(self):
        return '%s requires %s worship' % (self.feat.name, self.deity.name)

    def character_eligible(self, character):
        return character.deity == self.deity


class FeatArmorTypePrereq(FeatPrereq):
    armor = models.ForeignKey(ArmorType)

    class Meta:
        app_label = 'character_builder'

    def character_eligible(self, character):
        return CharacterArmorType.objects.filter(character=character, armor_type=self.armor).exists()


class FeatArmorOrArmorPrereq(FeatPrereq):
    allowed_armors = models.ManyToManyField(ArmorType)

    class Meta:
        app_label = 'character_builder'

    def character_eligible(self, character):
        return CharacterArmorType.objects.filter(armor_type__in=self.allowed_armors.all(), character=character).exists()
