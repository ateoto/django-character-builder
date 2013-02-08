from django.contrib import admin
from character_builder.models import (Source, Race, Role, Skill, Ability,
                                    CharacterSkill, CharacterAbility,
                                    ClassType, Character, Size,
                                    PowerType, Language,
                                    RaceAbilityMod, RaceSkillMod,
                                    Alignment, Deity, WeaponGroup,
                                    WeaponCategory, WeaponType,
                                    WeaponProficiencyGroup,
                                    ArmorClass, ArmorType,
                                    Currency, CurrencyExchange,
                                    CharacterCurrency, Gender, Party,
                                    Defense, ClassTypeDefMod,
                                    CharacterBaseDefense, ClassSkill,
                                    ClassFeature, AbilityPrerequisite,
                                    CharacterRaceFeature, CharacterClassFeature,
                                    RaceFeature)
from character_builder.models import (FeatRacePrereq, FeatClassTypePrereq,
                                        FeatClassFeaturePrereq, FeatAbilityPrereq,
                                        FeatSkillPrereq, FeatDeityPrereq, FeatSkillOrSkillPrereq,
                                        Feat)
from character_builder.models import (ClassPower, RacialPower, FeatPower)


class ClassTypeAdmin(admin.ModelAdmin):
    list_display = ('name', 'role', 'source')
    list_filter = ('source',)
    fields = ()


class CharacterAbilityAdmin(admin.ModelAdmin):
    list_display = ('character', 'ability', 'value')


admin.site.register(Source)
admin.site.register(Race)
admin.site.register(Role)
admin.site.register(Size)
admin.site.register(Skill)
admin.site.register(Ability)
admin.site.register(CharacterSkill)
admin.site.register(CharacterAbility, CharacterAbilityAdmin)
admin.site.register(ClassType, ClassTypeAdmin)
admin.site.register(Alignment)
admin.site.register(Deity)
admin.site.register(Character)
admin.site.register(PowerType)
admin.site.register(Language)
admin.site.register(RaceAbilityMod)
admin.site.register(RaceSkillMod)
admin.site.register(WeaponGroup)
admin.site.register(WeaponCategory)
admin.site.register(ArmorType)
admin.site.register(ArmorClass)
admin.site.register(Currency)
admin.site.register(CurrencyExchange)
admin.site.register(CharacterCurrency)
admin.site.register(Gender)
admin.site.register(WeaponType)
admin.site.register(WeaponProficiencyGroup)
admin.site.register(Party)
admin.site.register(Defense)
admin.site.register(ClassTypeDefMod)
admin.site.register(CharacterBaseDefense)
admin.site.register(ClassSkill)
admin.site.register(ClassFeature)
admin.site.register(AbilityPrerequisite)
admin.site.register(CharacterRaceFeature)
admin.site.register(CharacterClassFeature)
admin.site.register(RaceFeature)
admin.site.register(FeatRacePrereq)
admin.site.register(FeatClassTypePrereq)
admin.site.register(FeatClassFeaturePrereq)
admin.site.register(FeatAbilityPrereq)
admin.site.register(FeatSkillPrereq)
admin.site.register(FeatDeityPrereq)
admin.site.register(FeatSkillOrSkillPrereq)
admin.site.register(Feat)
admin.site.register(ClassPower)
admin.site.register(RacialPower)
admin.site.register(FeatPower)
