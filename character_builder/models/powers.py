from django.db import models

from .classtypes import ClassType
from .feats import Feat
from .races import Race
from .attributes import Ability

from model_utils.managers import InheritanceManager


class PowerKeyword(models.Model):
    name = models.CharField(max_length=50)

    class Meta:
        app_label = 'character_builder'

    def __unicode__(self):
        return self.name


class PowerType(models.Model):
    name = models.CharField(max_length=50)

    class Meta:
        app_label = 'character_builder'

    def __unicode__(self):
        return self.name


class PowerUsage(models.Model):
    name = models.CharField(max_length=50)

    class Meta:
        app_label = 'character_builder'

    def __unicode__(self):
        return self.name


class PowerRange(models.Model):
    name = models.CharField(max_length=50)

    class Meta:
        app_label = 'character_builder'

    def __unicode__(self):
        return self.name


class ActionType(models.Model):
    name = models.CharField(max_length=50)

    class Meta:
        app_label = 'character_builder'

    def __unicode__(self):
        return self.name


class Power(models.Model):
    name = models.CharField(max_length=50)
    flavor = models.TextField()
    level = models.IntegerField()
    power_type = models.ForeignKey(PowerType)
    action_type = models.ForeignKey(ActionType)
    range_type = models.ForeignKey(PowerRange)
    range_description = models.TextField(blank=True)
    keywords = models.ManyToManyField(PowerKeyword)
    usage = models.ForeignKey(PowerUsage)
    requirement = models.TextField(blank=True)
    target = models.TextField(blank=True)
    attack = models.TextField(blank=True)
    hit = models.TextField(blank=True)
    hit_modifier = models.ForeignKey(Ability, blank=True, null=True)
    secondary_target = models.TextField(blank=True)
    secondary_attack = models.TextField(blank=True)
    secondary_hit = models.TextField(blank=True)
    secondary_hit_modifier = models.ForeignKey(Ability, blank=True, null=True, related_name='secondary_hit_modifier')
    special = models.TextField(blank=True)
    miss = models.TextField(blank=True)
    secondary_target = models.TextField(blank=True)
    effect = models.TextField(blank=True)
    sustain = models.TextField(blank=True)
    sustain_action = models.ForeignKey(ActionType, blank=True, null=True, related_name='sustain_action')
    objects = InheritanceManager()

    class Meta:
        app_label = 'character_builder'

    def __unicode__(self):
        return self.name

    def line_detail(self):
        return Power.objects.get_subclass(id=self.id).line_detail()


class ClassPower(Power):
    class_type = models.ForeignKey(ClassType)

    class Meta:
        app_label = 'character_builder'

    def __unicode__(self):
        return self.name

    def line_detail(self):
        if self.level > 0:
            return "%s %s %i" % (self.class_type.name, self.power_type.name, self.level)
        else:
            return "%s %s" % (self.class_type.name, self.power_type.name)


class RacialPower(Power):
    race = models.ForeignKey(Race)

    class Meta:
        app_label = 'character_builder'

    def __unicode__(self):
        return self.name

    def line_detail(self):
        return "%s Racial Power" % (self.race.name)


class FeatPower(Power):
    feat = models.ForeignKey(Feat)

    class Meta:
        app_label = 'character_builder'

    def __unicode__(self):
        return self.name

    def line_detail(self):
        return "Feat Power"
