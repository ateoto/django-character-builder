from django.db import models

from .characteristics import (Source, Size, Vision, Language)
from .attributes import (Ability, Skill, Modifier)


class Race(models.Model):
    name = models.CharField(max_length=50)
    source = models.ForeignKey(Source)
    average_height_text = models.CharField(max_length=50)
    average_weight_text = models.CharField(max_length=50)
    size = models.ForeignKey(Size)
    speed = models.IntegerField()
    vision = models.ForeignKey(Vision)
    languages = models.ManyToManyField(Language)
    description = models.TextField()

    class Meta:
        app_label = 'character_builder'
        ordering = ['name']

    def __unicode__(self):
        return self.name


class RaceFeatureChoice(models.Model):
    name = models.CharField(max_length=100)
    benefit = models.TextField()

    class Meta:
        app_label = 'character_builder'

    def __unicode__(self):
        return self.name


class RaceFeature(models.Model):
    name = models.CharField(max_length=100)
    benefit = models.TextField()
    requires_choice = models.BooleanField(default=False)
    choices = models.ManyToManyField(RaceFeatureChoice, blank=True)
    race = models.ForeignKey(Race)
    has_passive_effects = models.BooleanField(default=False)
    passive_effects = models.ManyToManyField(Modifier, blank=True)

    class Meta:
        app_label = 'character_builder'

    def __unicode__(self):
        return "%s: %s" % (self.race.name, self.name)


class RaceAbilityMod(models.Model):
    race = models.ForeignKey(Race, related_name="ability_mods")
    ability = models.ForeignKey(Ability)
    modifier = models.IntegerField()

    class Meta:
        app_label = 'character_builder'

    def __unicode__(self):
        if self.modifier < 0:
            mod = "-"
        elif self.modifier == 0:
            mod = ""
        else:
            mod = "+"

        return "%s: %s%s %s" % (self.race.name, mod, self.modifier, self.ability.name)

    def pretty(self):
        if self.modifier < 0:
            mod = "-"
        elif self.modifier == 0:
            mod = ""
        else:
            mod = "+"

        return "%s%s %s" % (mod, self.modifier, self.ability.name)


class RaceSkillMod(models.Model):
    race = models.ForeignKey(Race, related_name='skill_mods')
    skill = models.ForeignKey(Skill)
    modifier = models.IntegerField()

    class Meta:
        app_label = 'character_builder'

    def __unicode__(self):
        if self.modifier < 0:
            mod = "-"
        elif self.modifier == 0:
            mod = ""
        else:
            mod = "+"

        return "%s: %s%s %s" % (self.race.name, mod, self.modifier, self.skill.name)

