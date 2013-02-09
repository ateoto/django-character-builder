from django.db import models

from .classtypes import ClassType
from .feats import Feat
from .races import Race


class PowerType(models.Model):
    name = models.CharField(max_length=50)

    class Meta:
        app_label = 'character_builder'

    def __unicode__(self):
        return self.name


class PowerKeyword(models.Model):
    name = models.CharField(max_length=50)

    class Meta:
        app_label = 'character_builder'

    def __unicode__(self):
        return self.name


class Power(models.Model):
    name = models.CharField(max_length=100)
    level = models.IntegerField()
    power_type = models.ForeignKey(PowerType)
    flavor = models.TextField(blank=True, null=True)
    keywords = models.TextField(blank=True, null=True)
    target = models.TextField(blank=True, null=True)
    attack = models.TextField(blank=True, null=True)
    hit = models.TextField(blank=True, null=True)
    miss = models.TextField(blank=True, null=True)
    effect = models.TextField(blank=True, null=True)
    special = models.TextField(blank=True, null=True)

    class Meta:
        app_label = 'character_builder'

    def __unicode__(self):
        return self.name


class ClassPower(Power):
    class_type = models.ForeignKey(ClassType)

    class Meta:
        app_label = 'character_builder'


class RacialPower(Power):
    race = models.ForeignKey(Race)

    class Meta:
        app_label = 'character_builder'

    def __unicode__(self):
        return self.name


class FeatPower(Power):
    feat = models.ForeignKey(Feat)

    class Meta:
        app_label = 'character_builder'
