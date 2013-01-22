from django.db import models
from django.contrib.auth.models import User


class Source(models.Model):
    name = models.CharField(max_length=50)

    class Meta:
        ordering = ['name']

    def __unicode__(self):
        return self.name


class Campaign(models.Model):
    name = models.CharField(max_length=100)
    dm = models.ForeignKey(User, related_name="+")
    players = models.ManyToManyField(User, related_name="+")

    def __unicode__(self):
        return self.name


class Role(models.Model):
    name = models.CharField(max_length=50)

    def __unicode__(self):
        return self.name


class Size(models.Model):
    name = models.CharField(max_length=50)
    space = models.CharField(max_length=50)
    reach = models.CharField(max_length=50)

    def __unicode__(self):
        return self.name


class Gender(models.Model):
    name = models.CharField(max_length=25)

    def __unicode__(self):
        return self.name


class Language(models.Model):
    name = models.CharField(max_length=50)
    script = models.CharField(max_length=50)

    def __unicode__(self):
        return self.name


class Vision(models.Model):
    name = models.CharField(max_length=50)

    def __unicode__(self):
        return self.name


class Ability(models.Model):
    name = models.CharField(max_length=50)
    abbreviation = models.CharField(max_length=4)
    help_text = models.TextField()

    class Meta:
        verbose_name_plural = "Abilities"

    def __unicode__(self):
        return self.name


class Skill(models.Model):
    name = models.CharField(max_length=50)
    ability = models.ForeignKey(Ability)

    def __unicode__(self):
        return self.name


class PowerType(models.Model):
    name = models.CharField(max_length=50)

    def __unicode__(self):
        return self.name


class PowerKeyword(models.Model):
    name = models.CharField(max_length=50)

    def __unicode__(self):
        return self.name


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
        ordering = ['name']

    def __unicode__(self):
        return self.name


class RaceAbilityMod(models.Model):
    race = models.ForeignKey(Race)
    ability = models.ForeignKey(Ability)
    modifier = models.IntegerField()

    def __unicode__(self):
        if self.modifier < 0:
            mod = "-"
        elif self.modifier == 0:
            mod = ""
        else:
            mod = "+"

        return "%s: %s%s %s" % (self.race.name, mod, self.modifier, self.ability.name)


class RaceSkillMod(models.Model):
    race = models.ForeignKey(Race)
    skill = models.ForeignKey(Skill)
    modifier = models.IntegerField()

    def __unicode__(self):
        if self.modifier < 0:
            mod = "-"
        elif self.modifier == 0:
            mod = ""
        else:
            mod = "+"

        return "%s: %s%s %s" % (self.race.name, mod, self.modifier, self.skill.name)


class WeaponCategory(models.Model):
    name = models.CharField(max_length=50)

    def __unicode__(self):
        return self.name


class WeaponGroup(models.Model):
    name = models.CharField(max_length=50)

    def __unicode__(self):
        return self.name


class WeaponProficiencyGroup(models.Model):
    name = models.CharField(max_length=50)
    categories = models.ManyToManyField(WeaponCategory)

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

    def __unicode__(self):
        return self.name


class ArmorClass(models.Model):
    name = models.CharField(max_length=50)

    def __unicode__(self):
        return self.name


class ArmorType(models.Model):
    name = models.CharField(max_length=50)
    armor_class = models.ForeignKey(ArmorClass)

    def __unicode__(self):
        return self.name


class ClassType(models.Model):
    name = models.CharField(max_length=100)
    role = models.ForeignKey(Role)
    role_flavor = models.TextField()
    source = models.ForeignKey(Source)
    favored_abilities = models.ManyToManyField(Ability)
    description = models.TextField()
    weapon_proficiencies = models.ManyToManyField(WeaponProficiencyGroup)
    armor_proficiencies = models.ManyToManyField(ArmorType)

    class Meta:
        ordering = ['name']

    def __unicode__(self):
        return self.name


class Power(models.Model):
    name = models.CharField(max_length=100)
    level = models.IntegerField()
    class_type = models.ForeignKey(ClassType, blank=True, null=True)
    race = models.ForeignKey(Race, blank=True, null=True)
    power_type = models.ForeignKey(PowerType)
    flavor = models.TextField(blank=True)
    keywords = models.TextField()
    target = models.TextField(blank=True)
    attack = models.TextField(blank=True)
    hit = models.TextField(blank=True)
    miss = models.TextField(blank=True)
    effect = models.TextField(blank=True)
    special = models.TextField(blank=True)

    def __unicode__(self):
        return self.name


class Alignment(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField()

    def __unicode__(self):
        return self.name


class Deity(models.Model):
    name = models.CharField(max_length=100)
    alignment = models.ForeignKey(Alignment)
    description = models.TextField()

    def __unicode__(self):
        return self.name


class Currency(models.Model):
    name = models.CharField(max_length=25)
    abbreviation = models.CharField(max_length=3)
    weight = models.DecimalField(max_digits=6, decimal_places=3)

    def __unicode__(self):
        return self.name


class CurrencyExchange(models.Model):
    currency_from = models.ForeignKey(Currency, related_name="+")
    currency_to = models.ForeignKey(Currency, related_name="+")
    exchange_rate = models.DecimalField(max_digits=18, decimal_places=9)

    def __unicode__(self):
        return "%s to %s" % (self.currency_from.name, self.currency_to.name)


class Character(models.Model):
    user = models.ForeignKey(User, related_name="+")
    name = models.CharField(max_length=100)
    class_type = models.ForeignKey(ClassType)
    race = models.ForeignKey(Race)
    gender = models.ForeignKey(Gender)
    level = models.IntegerField(default=1, blank=True)
    xp = models.IntegerField(default=0, blank=True)
    hit_points = models.IntegerField(blank=True, null=True)
    age = models.IntegerField(blank=True, null=True)
    weight = models.CharField(max_length=20, blank=True, null=True)
    height = models.CharField(max_length=20, blank=True, null=True)
    alignment = models.ForeignKey(Alignment)
    deity = models.ForeignKey(Deity)

    def __unicode__(self):
        return "%s Level %i %s %s" % (self.name, self.level, self.race.name, self.class_type.name)


class CharacterCurrency(models.Model):
    character = models.ForeignKey(Character, related_name="wealth")
    currency_type = models.ForeignKey(Currency)
    amount = models.IntegerField(default=0)

    def __unicode__(self):
        return "%s's coin purse." % (self.character.name)


class CharacterAbility(models.Model):
    character = models.ForeignKey(Character, related_name="abilities")
    ability = models.ForeignKey(Ability)
    value = models.IntegerField()

    class Meta:
        verbose_name_plural = "Character Abilities"

    def __unicode__(self):
        return "%s %s" % (self.ability.name, self.value)


class CharacterSkill(models.Model):
    character = models.ForeignKey(Character, related_name="skills")
    skill = models.ForeignKey(Skill)
    is_trained = models.BooleanField(default=False)
    value = models.IntegerField()

    def __unicode__(self):
        return "%s %s" % (self.skill.name, self.value)


class CharacterPower(models.Model):
    character = models.ForeignKey(Character, related_name="powers")
    power = models.ForeignKey(Power)


class Item(models.Model):
    name = models.CharField(max_length=100)
    source = models.ForeignKey(Source)

    def __unicode__(self):
        return self.name


class Party(models.Model):
    name = models.CharField(max_length=100)
    characters = models.ManyToManyField(Character, related_name="party")
    formed = models.DateField()

    def __unicode__(self):
        return self.name
