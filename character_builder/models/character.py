from django.db import models
from django.contrib.auth.models import User
from django.template.defaultfilters import slugify

from .characteristics import (Deity, Gender, Alignment, Level)
from .attributes import (Ability, Skill, Defense)
from .feats import (Feat)
from .powers import (Power)
from .races import (Race, RaceFeature, RaceFeatureChoice)
from .classtypes import (ClassType, ClassFeature, ClassFeatureChoice)
from .items import (ArmorType, Currency)

import math


class Character(models.Model):
    user = models.ForeignKey(User, related_name="+")
    name = models.CharField(max_length=100)
    slug_name = models.SlugField()
    class_type = models.ForeignKey(ClassType)
    race = models.ForeignKey(Race)
    gender = models.ForeignKey(Gender)
    xp = models.IntegerField(default=0, blank=True)
    max_hit_points = models.IntegerField(default=0, blank=True, null=True)
    hit_points = models.IntegerField(default=0, blank=True)
    age = models.IntegerField(blank=True, null=True)
    weight = models.CharField(max_length=20, blank=True, null=True)
    height = models.CharField(max_length=20, blank=True, null=True)
    alignment = models.ForeignKey(Alignment)
    deity = models.ForeignKey(Deity)

    class Meta:
        app_label = 'character_builder'

    def __unicode__(self):
        return "%s Level %i %s %s" % (self.name, self.current_level().number, self.race.name, self.class_type.name)

    def save(self, *args, **kwargs):
        if not self.id:
            self.slug_name = slugify(self.name)

        super(Character, self).save(*args, **kwargs)

    @models.permalink
    def get_absolute_url(self):
        return ('character-builder-sheet', (), {
            'character_slug': self.slug_name})

    def calc_hit_points(self):
        level = self.current_level().number
        if level == 1:
            level = 0

        level_mod = self.class_type.hit_points_per_level * level

        self.max_hit_points = level_mod + self.class_type.base_hit_points + self.abilities.get(ability__name='Constitution').value
        self.save()

    def get_defenses(self):
        #get table of modifiers
        response = {}

        for defense in Defense.objects.all():
            base = int(10 + (math.floor(self.current_level().number / 2)))
            armor = False  # This needs to check the character's current equipped armor, which requires I work that out.
            abil = max([abil.modifier_half_level() for abil in CharacterAbility.objects.filter(character=self, ability__in=defense.abilities.all())])

            classtype = []
            for class_mod in self.class_type.modifiers.all().select_subclasses():
                if hasattr(class_mod, 'defense'):
                    if class_mod.defense == defense:
                        classtype.append(class_mod.value)
            classtype = sum(classtype)

            race = []
            for race_mod in self.race.modifiers.all().select_subclasses():
                if hasattr(race_mod, 'defense'):
                    if race_mod.defense == defense:
                        race.append(race_mod.value)
            race = sum(race)

            response[defense.abbreviation.lower()] = {
                'base': base,
                'armor': armor,
                'abil': abil,
                'classtype': classtype,
                'race': race,
                'total': sum([base, armor, abil, classtype, race])
            }

        return response

    def current_level(self):
        return Level.objects.order_by('-xp_required').filter(xp_required__lte=self.xp)[:1].get()

    def next_level(self):
        try:
            return Level.objects.get(number=self.current_level().number + 1)
        except:
            return self.current_level

    def extended_rest(self):
        self.calc_hit_points()
        self.hit_points = self.max_hit_points
        self.save()


class CharacterCurrency(models.Model):
    character = models.ForeignKey(Character, related_name="wealth")
    currency_type = models.ForeignKey(Currency)
    amount = models.IntegerField(default=0)

    class Meta:
        app_label = 'character_builder'

    def __unicode__(self):
        return "%s's coin purse." % (self.character.name)


class CharacterRaceFeature(models.Model):
    character = models.ForeignKey(Character, related_name="race_features")
    race_feature = models.ForeignKey(RaceFeature)
    benefit = models.TextField()

    class Meta:
        app_label = 'character_builder'

    def __unicode__(self):
        return "%s : %s" % (self.character.name, self.race_feature.name)


class CharacterClassFeature(models.Model):
    character = models.ForeignKey(Character, related_name="class_features")
    class_feature = models.ForeignKey(ClassFeature)
    choice = models.ForeignKey(ClassFeatureChoice, null=True, blank=True)

    class Meta:
        app_label = 'character_builder'

    def __unicode__(self):
        return "%s : %s" % (self.character.name, self.class_feature.name)


class CharacterAbility(models.Model):
    character = models.ForeignKey(Character, related_name="abilities")
    ability = models.ForeignKey(Ability)
    value = models.IntegerField()

    class Meta:
        app_label = 'character_builder'
        verbose_name_plural = "Character Abilities"

    def modifier(self):
        return int(math.floor((math.fabs(self.value) - 10) / 2))

    def modifier_half_level(self):
        return self.modifier() + int(math.floor(self.character.current_level().number / 2))

    def __unicode__(self):
        return "%s %s" % (self.ability.name, self.value)


class CharacterArmorType(models.Model):
    character = models.ForeignKey(Character, related_name="armor_types")
    armor_type = models.ForeignKey(ArmorType)

    class Meta:
        app_label = 'character_builder'


class CharacterSkill(models.Model):
    character = models.ForeignKey(Character, related_name="skills")
    skill = models.ForeignKey(Skill)
    is_trained = models.BooleanField(default=False)
    value = models.IntegerField()

    class Meta:
        app_label = 'character_builder'

    def __unicode__(self):
        return "%s: %s %s" % (self.character.name, self.skill.name, self.value)

    def modifier_half_level(self):
        if self.is_trained:
            training_mod = 5
        else:
            training_mod = 0

        ability_mod = CharacterAbility.objects.get(
                            character=self.character,
                            ability=self.skill.ability).modifier_half_level()

        return sum([self.value, training_mod,
                    ability_mod, int(math.floor(self.character.current_level().number / 2))])


class CharacterFeat(models.Model):
    character = models.ForeignKey(Character, related_name="feats")
    feat = models.ForeignKey(Feat)
    required_choice = models.BooleanField(default=False)
    choice_result = models.TextField(blank=True)

    class Meta:
        app_label = 'character_builder'

    def __unicode__(self):
        return "%s: %s" % (self.character.name, self.feat.name)


class CharacterPower(models.Model):
    character = models.ForeignKey(Character, related_name="powers")
    power = models.ForeignKey(Power)

    class Meta:
        app_label = 'character_builder'
