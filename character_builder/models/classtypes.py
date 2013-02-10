from django.db import models

from .characteristics import (Source, Role)
from .attributes import (Ability, Skill, Defense, Modifier)
from .items import (WeaponProficiencyGroup, ArmorType)


class ClassType(models.Model):
    name = models.CharField(max_length=100)
    role = models.ForeignKey(Role)
    role_flavor = models.TextField()
    source = models.ForeignKey(Source)
    favored_abilities = models.ManyToManyField(Ability)
    description = models.TextField()
    modifiers = models.ManyToManyField(Modifier, blank=True)
    weapon_proficiencies = models.ManyToManyField(WeaponProficiencyGroup)
    armor_proficiencies = models.ManyToManyField(ArmorType)
    trained_skills = models.ManyToManyField(Skill, blank=True, null=True)
    skill_choices = models.IntegerField(default=3)
    base_hit_points = models.IntegerField(default=0)
    hit_points_per_level = models.IntegerField(default=0)

    class Meta:
        app_label = 'character_builder'
        ordering = ['name']

    def __unicode__(self):
        return self.name


class ClassFeatureChoice(models.Model):
    name = models.CharField(max_length=100)
    benefit = models.TextField()

    class Meta:
        app_label = 'character_builder'

    def __unicode__(self):
        return self.name


class ClassFeature(models.Model):
    name = models.CharField(max_length=100)
    benefit = models.TextField()
    requires_choice = models.BooleanField(default=False)
    choices = models.ManyToManyField(ClassFeatureChoice, blank=True)
    class_type = models.ManyToManyField(ClassType)
    passive_effects = models.ManyToManyField(Modifier, blank=True)

    class Meta:
        app_label = 'character_builder'

    def __unicode__(self):
        class_types = ''
        cts = self.class_type.all()
        if cts.count() > 1:
            for ct in cts:
                class_types += ct.name + ' / '
            class_types = class_types[:-3]
        else:
            class_types = cts[:1].get().name

        return "%s: %s" % (class_types, self.name)


class ClassTypeDefMod(models.Model):
    class_type = models.ForeignKey(ClassType)
    defense = models.ForeignKey(Defense)
    bonus = models.IntegerField()

    class Meta:
        app_label = 'character_builder'

    def __unicode__(self):
        return "%s: %s to %s" % (self.class_type.name, self.bonus, self.defense.name)


class ClassSkill(models.Model):
    class_type = models.ForeignKey(ClassType, related_name="class_skills")
    skill = models.ForeignKey(Skill)

    class Meta:
        app_label = 'character_builder'

    def __unicode__(self):
        return "%s %s" % (self.class_type.name, self.skill.name)
