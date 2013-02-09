from django.db import models

from model_utils.managers import InheritanceManager


class Ability(models.Model):
    name = models.CharField(max_length=50)
    abbreviation = models.CharField(max_length=4)
    help_text = models.TextField()

    class Meta:
        app_label = 'character_builder'
        verbose_name_plural = "Abilities"

    def __unicode__(self):
        return self.name


class Skill(models.Model):
    name = models.CharField(max_length=50)
    ability = models.ForeignKey(Ability)

    class Meta:
        app_label = 'character_builder'

    def __unicode__(self):
        return self.name


class Defense(models.Model):
    name = models.CharField(max_length=20)
    abbreviation = models.CharField(max_length=10)

    class Meta:
        app_label = 'character_builder'

    def __unicode__(self):
        return self.name


class Modifier(models.Model):
    objects = InheritanceManager()

    class Meta:
        app_label = 'character_builder'


class AbilityMod(Modifier):
    ability = models.ForeignKey(Ability)
    value = models.IntegerField()

    class Meta:
        app_label = 'character_builder'


    def apply_mod(self, character):
        raise NotImplemented

    def pretty(self):
        if self.value < 0:
            mod = "-"
        elif self.value == 0:
            mod = ""
        else:
            mod = "+"

        return "%s%s %s" % (mod, self.value, self.ability.name)


class SkillMod(Modifier):
    skill = models.ForeignKey(Skill)
    value = models.IntegerField()

    class Meta:
        app_label = 'character_builder'

    def apply_mod(self, character):
        raise NotImplemented

    def pretty(self):
        if self.value < 0:
            mod = "-"
        elif self.value == 0:
            mod = ""
        else:
            mod = "+"

        return "%s%s %s" % (mod, self.value, self.skill.name)


class DefenseMod(Modifier):
    defense = models.ForeignKey(Defense)
    value = models.IntegerField()

    class Meta:
        app_label = 'character_builder'

    def apply_mod(self, character):
        raise NotImplemented

    def pretty(self):
        if self.value < 0:
            mod = "-"
        elif self.value == 0:
            mod = ""
        else:
            mod = "+"

        return "%s%s %s" % (mod, self.value, self.defense.name)