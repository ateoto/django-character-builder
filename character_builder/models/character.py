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
            'character_id': self.id,
            'character_slug': self.slug_name})

    def init_hit_points(self):
        self.max_hit_points = self.class_type.base_hit_points + self.abilities.get(ability__name='Constitution').value
        self.hit_points = self.max_hit_points
        self.save()

    def current_level(self):
        return Level.objects.order_by('-xp_required').filter(xp_required__lte=self.xp)[:1].get()

    def next_level(self):
        try:
            return Level.objects.get(number=self.current_level().number + 1)
        except:
            return self.current_level


class CharacterCurrency(models.Model):
    character = models.ForeignKey(Character, related_name="wealth")
    currency_type = models.ForeignKey(Currency)
    amount = models.IntegerField(default=0)

    class Meta:
        app_label = 'character_builder'

    def __unicode__(self):
        return "%s's coin purse." % (self.character.name)


class CharacterBaseDefense(models.Model):
    character = models.ForeignKey(Character, related_name="defenses")
    defense = models.ForeignKey(Defense)
    value = models.IntegerField()

    class Meta:
        app_label = 'character_builder'

    def __unicode__(self):
        return "%s %s" % (self.defense.name, self.value)


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