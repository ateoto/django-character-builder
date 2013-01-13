from django.db import models
from django.contrib.auth.models import User

class Source(models.Model):
    name = models.CharField(max_length = 50)
    
    class Meta:
        ordering = ['name']

    def __unicode__(self):
        return self.name

class Campaign(models.Model):
    name = models.CharField(max_length = 100)
    dm = models.ForeignKey(User, related_name = "+")
    players = models.ManyToManyField(User, related_name = "+")

    def __unicode__(self):
        return self.name

class Role(models.Model):
    name = models.CharField(max_length = 50)

    def __unicode__(self):
        return self.name

class Size(models.Model):
    name = models.CharField(max_length = 50)
    space = models.CharField(max_length = 50)
    reach = models.CharField(max_length = 50)

    def __unicode__(self):
        return self.name

class Vision(models.Model):
    name = models.CharField(max_length = 50)

    def __unicode__(self):
        return self.name

class Ability(models.Model):
    name = models.CharField(max_length = 50)
    abbreviation = models.CharField(max_length = 4)

    class Meta:
        verbose_name_plural = "Abilities"

    def __unicode__(self):
        return self.name

class Skill(models.Model):
    name = models.CharField(max_length = 50)
    ability = models.ForeignKey(Ability)

    def __unicode__(self):
        return self.name

class CharacterAbility(models.Model):
    character = models.ForeignKey('Character')
    ability = models.ForeignKey(Ability)
    value = models.IntegerField()
    
    class Meta:
        verbose_name_plural = "Character Abilities"

    def __unicode__(self):
        return "%s %s" % (self.ability.name, self.value)

class CharacterSkill(models.Model):
    character = models.ForeignKey('Character')
    skill = models.ForeignKey(Skill)
    is_trained = models.BooleanField(default = False)
    value = models.IntegerField()

    def __unicode__(self):
        return "%s %s" % (self.skill.name, self.value)

class Race(models.Model):
    name = models.CharField(max_length = 50)
    source = models.ForeignKey(Source)
    average_height_text = models.CharField(max_length = 50)
    average_weight_text = models.CharField(max_length = 50)
    size = models.ForeignKey(Size)
    speed = models.IntegerField()
    vision = models.ForeignKey(Vision)
    description = models.TextField()

    class Meta:
        ordering = ['name']

    def __unicode__(self):
        return self.name

class RaceAbilityMod(models.Model):
    race = models.ForeignKey(Race)
    abilty = models.ForeignKey(Ability)
    modifier = models.IntegerField()

class RaceSkillMod(models.Model):
    race = models.ForeignKey(Race)
    skill = models.ForeignKey(Skill)
    modifier = models.IntegerField()

class ClassType(models.Model):
    name = models.CharField(max_length = 100)
    role = models.ForeignKey(Role)
    source = models.ForeignKey(Source)
    
    class Meta:
        ordering = ['name']

    def __unicode__(self):
        return self.name

class Character(models.Model):
    user = models.ForeignKey(User, related_name="+")
    name = models.CharField(max_length = 100)
    class_type = models.ForeignKey(ClassType)
    race = models.ForeignKey(Race)
    level = models.IntegerField()
    xp = models.IntegerField()
    hit_points = models.IntegerField()

    def __unicode__(self):
        return "%s Level %i %s %s" % (self.name, self.level, self.race.name, self.class_type.name)

class Item(models.Model):
    name = models.CharField(max_length = 100)
    source = models.ForeignKey(Source)

    def __unicode__(self):
        return self.name
