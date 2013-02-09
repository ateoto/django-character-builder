from django.db import models

from .characteristics import (Source)


class WeaponCategory(models.Model):
    name = models.CharField(max_length=50)

    class Meta:
        app_label = 'character_builder'

    def __unicode__(self):
        return self.name


class WeaponGroup(models.Model):
    name = models.CharField(max_length=50)

    class Meta:
        app_label = 'character_builder'

    def __unicode__(self):
        return self.name


class WeaponProficiencyGroup(models.Model):
    name = models.CharField(max_length=50)
    categories = models.ManyToManyField(WeaponCategory)

    class Meta:
        app_label = 'character_builder'

    def __unicode__(self):
        return self.name


class WeaponType(models.Model):
    name = models.CharField(max_length=50)
    category = models.ForeignKey(WeaponCategory)
    group = models.ForeignKey(WeaponGroup)
    proficiency = models.CharField(max_length=10)
    damage = models.CharField(max_length=10)
    weapon_range = models.CharField(max_length=10)
    properties = models.TextField(blank=True, null=True)

    class Meta:
        app_label = 'character_builder'

    def __unicode__(self):
        return self.name


class ArmorClass(models.Model):
    name = models.CharField(max_length=50)

    class Meta:
        app_label = 'character_builder'

    def __unicode__(self):
        return self.name


class ArmorType(models.Model):
    name = models.CharField(max_length=50)
    armor_class = models.ForeignKey(ArmorClass)

    class Meta:
        app_label = 'character_builder'

    def __unicode__(self):
        return self.name


class Currency(models.Model):
    name = models.CharField(max_length=25)
    abbreviation = models.CharField(max_length=3)
    weight = models.DecimalField(max_digits=6, decimal_places=3)

    class Meta:
        app_label = 'character_builder'

    def __unicode__(self):
        return self.name


class CurrencyExchange(models.Model):
    currency_from = models.ForeignKey(Currency, related_name="+")
    currency_to = models.ForeignKey(Currency, related_name="+")
    exchange_rate = models.DecimalField(max_digits=18, decimal_places=9)

    class Meta:
        app_label = 'character_builder'

    def __unicode__(self):
        return "%s to %s" % (self.currency_from.name, self.currency_to.name)


class Item(models.Model):
    name = models.CharField(max_length=100)
    source = models.ForeignKey(Source)

    class Meta:
        app_label = 'character_builder'

    def __unicode__(self):
        return self.name
