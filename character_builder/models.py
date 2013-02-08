from django.db import models
from django.contrib.auth.models import User
from django.template.defaultfilters import slugify
from django.core.exceptions import ObjectDoesNotExist

from json_field import JSONField
from model_utils.managers import InheritanceManager

import math


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
    race = models.ForeignKey(Race, related_name="ability_mods")
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
    trained_skills = models.ManyToManyField(Skill, blank=True, null=True)
    skill_choices = models.IntegerField(default=3)
    base_hit_points = models.IntegerField(default=0)
    hit_points_per_level = models.IntegerField(default=0)

    class Meta:
        ordering = ['name']

    def __unicode__(self):
        return self.name


class Defense(models.Model):
    name = models.CharField(max_length=20)
    abbreviation = models.CharField(max_length=10)

    def __unicode__(self):
        return self.name


class ClassTypeDefMod(models.Model):
    class_type = models.ForeignKey(ClassType)
    defense = models.ForeignKey(Defense)
    bonus = models.IntegerField()

    def __unicode__(self):
        return "%s: %s to %s" % (self.class_type.name, self.bonus, self.defense.name)


class ClassSkill(models.Model):
    class_type = models.ForeignKey(ClassType, related_name="class_skills")
    skill = models.ForeignKey(Skill)

    def __unicode__(self):
        return "%s %s" % (self.class_type.name, self.skill.name)


class AbilityPrerequisite(models.Model):
    ability = models.ForeignKey(Ability)
    value = models.IntegerField()

    def __unicode__(self):
        return "%s %s" % (self.ability.name, self.value)


class Alignment(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField()

    def __unicode__(self):
        return self.name


class Level(models.Model):
    number = models.IntegerField()
    xp_required = models.IntegerField()

    def __unicode__(self):
        return "%s: %s xp required" % (self.number, self.xp_required)


class Deity(models.Model):
    name = models.CharField(max_length=100)
    alignment = models.ForeignKey(Alignment)
    description = models.TextField()

    def __unicode__(self):
        return self.name


class ClassFeature(models.Model):
    name = models.CharField(max_length=100)
    benefit = models.TextField()
    requires_choice = models.BooleanField(default=False)
    choices_json = JSONField(blank=True)
    class_type = models.ManyToManyField(ClassType)
    has_passive_effects = models.BooleanField(default=False)
    passive_effects = JSONField(default='{}', blank=True)

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


class RaceFeature(models.Model):
    name = models.CharField(max_length=100)
    benefit = models.TextField()
    requires_choice = models.BooleanField(default=False)
    choices_json = JSONField(blank=True)
    race = models.ForeignKey(Race)
    has_passive_effects = models.BooleanField(default=False)
    passive_effects = JSONField(default='{}', blank=True)

    def __unicode__(self):
        return "%s: %s" % (self.race.name, self.name)


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

    def __unicode__(self):
        return self.name


class ClassPower(Power):
    class_type = models.ForeignKey(ClassType)


class RacialPower(Power):
    race = models.ForeignKey(Race)

    def __unicode__(self):
        return self.name


# Feats
class FeatManager(models.Manager):
    def eligible_for_character(self, character):
        qs = super(FeatManager, self).get_query_set()
        for feat in qs:
            if not feat.character_eligible(character):
                qs = qs.exclude(id=feat.id)

        return qs


class Feat(models.Model):
    name = models.CharField(max_length=50)
    benefit = models.TextField()
    special = models.TextField(blank=True)
    has_passive_effects = models.BooleanField(default=False)
    passive_effects = JSONField(default='{}', blank=True)
    objects = FeatManager()

    def character_eligible(self, character):
        eligible = []
        for prereq in FeatPrereq.objects.filter(feat=self).select_subclasses():
            eligible.append(prereq.character_eligible(character))

        return all(eligible)

    def __unicode__(self):
        return self.name


class FeatPrereq(models.Model):
    feat = models.ForeignKey(Feat, related_name='prereqs')
    objects = InheritanceManager()


class FeatRacePrereq(FeatPrereq):
    race = models.ForeignKey(Race)

    def character_eligible(self, character):
        return self.race == character.race

    def __unicode__(self):
        return '%s requires %s' % (self.feat.name, self.race.name)


class FeatClassTypePrereq(FeatPrereq):
    class_type = models.ForeignKey(ClassType)

    def character_eligible(self, character):
        return self.class_type == character.class_type

    def __unicode__(self):
        return '%s requires %s' % (self.feat.name, self.class_type.name)


class FeatClassFeaturePrereq(FeatPrereq):
    classfeature = models.ForeignKey(ClassFeature)

    def character_eligible(self, character):
            return character.class_features.filter(class_feature=self.classfeature).exists()

    def __unicode__(self):
        return '%s requires %s' % (self.feat.name, self.classfeature.name)


class FeatAbilityPrereq(FeatPrereq):
    ability = models.ForeignKey(Ability)
    value = models.IntegerField()

    def character_eligible(self, character):
        ca = CharacterAbility.objects.get(ability=self.ability, character=character)
        return ca.value >= self.value

    def __unicode__(self):
        return '%s requires %s %i' % (self.feat.name, self.ability.name, self.value)


class FeatSkillPrereq(FeatPrereq):
    skill = models.ForeignKey(Skill)

    def character_eligible(self, character):
        return CharacterSkill.objects.filter(skill=self.skill, character=character, is_trained=True).exists()


class FeatSkillOrSkillPrereq(FeatPrereq):
    allowed_skills = models.ManyToManyField(Skill)

    def character_eligible(self, character):
        return CharacterSkill.objects.filter(skill__in=self.allowed_skills.all(), character=character, is_trained=True).exists()


class FeatFeatPrereq(FeatPrereq):
    pre_feat = models.ForeignKey(Feat)

    def character_eligible(self, character):
        CharacterFeat.objects.get(feat=self.pre_feat, character=character).exists()


class FeatDeityPrereq(FeatPrereq):
    deity = models.ForeignKey(Deity)

    def character_eligible(self, character):
        return character.deity == self.deity

    def __unicode__(self):
        return '%s requires %s worship' % (self.feat.name, self.deity.name)


class FeatArmorTypePrereq(FeatPrereq):
    armor = models.ForeignKey(ArmorType)

    def character_eligible(self, character):
        return CharacterArmorType.objects.filter(character=character, armor_type=self.armor).exists()


class FeatArmorOrArmorPrereq(FeatPrereq):
    allowed_armors = models.ManyToManyField(ArmorType)

    def character_eligible(self, character):
        return CharacterArmorType.objects.filter(armor_type__in=self.allowed_armors.all(), character=character).exists()


class FeatPower(Power):
    feat = models.ForeignKey(Feat)


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


class CharacterCurrency(models.Model):
    character = models.ForeignKey(Character, related_name="wealth")
    currency_type = models.ForeignKey(Currency)
    amount = models.IntegerField(default=0)

    def __unicode__(self):
        return "%s's coin purse." % (self.character.name)


class CharacterBaseDefense(models.Model):
    character = models.ForeignKey(Character, related_name="defenses")
    defense = models.ForeignKey(Defense)
    value = models.IntegerField()

    def __unicode__(self):
        return "%s %s" % (self.defense.name, self.value)


class CharacterRaceFeature(models.Model):
    character = models.ForeignKey(Character, related_name="race_features")
    race_feature = models.ForeignKey(RaceFeature)
    benefit = models.TextField()

    def __unicode__(self):
        return "%s : %s" % (self.character.name, self.race_feature.name)


class CharacterClassFeature(models.Model):
    character = models.ForeignKey(Character, related_name="class_features")
    class_feature = models.ForeignKey(ClassFeature)
    benefit = models.TextField()

    def __unicode__(self):
        return "%s : %s" % (self.character.name, self.class_feature.name)


class CharacterAbility(models.Model):
    character = models.ForeignKey(Character, related_name="abilities")
    ability = models.ForeignKey(Ability)
    value = models.IntegerField()

    class Meta:
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


class CharacterSkill(models.Model):
    character = models.ForeignKey(Character, related_name="skills")
    skill = models.ForeignKey(Skill)
    is_trained = models.BooleanField(default=False)
    value = models.IntegerField()

    def __unicode__(self):
        return "%s: %s %s" % (self.character.name, self.skill.name, self.value)


class CharacterFeat(models.Model):
    character = models.ForeignKey(Character, related_name="feats")
    feat = models.ForeignKey(Feat)

    def __unicode__(self):
        return "%s: %s" % (self.character.name, self.feat.name)


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
