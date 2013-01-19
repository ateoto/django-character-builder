from django.contrib import admin
from character_builder.models import (Source, Race, Role, Skill, Ability,
                                    CharacterSkill, CharacterAbility,
                                    ClassType, Character, Size,
                                    PowerType, Power, Language,
                                    RaceAbilityMod, RaceSkillMod,
                                    Alignment, Deity, WeaponGroup,
                                    WeaponCategory, WeaponType,
                                    ArmorClass, ArmorType,
                                    Currency, CurrencyExchange,
                                    CharacterCurrency, Gender)


class ClassTypeAdmin(admin.ModelAdmin):
    list_display = ('name', 'role', 'source')
    list_filter = ('source',)


admin.site.register(Source)
admin.site.register(Race)
admin.site.register(Role)
admin.site.register(Size)
admin.site.register(Skill)
admin.site.register(Ability)
admin.site.register(CharacterSkill)
admin.site.register(CharacterAbility)
admin.site.register(ClassType, ClassTypeAdmin)
admin.site.register(Alignment)
admin.site.register(Deity)
admin.site.register(Character)
admin.site.register(PowerType)
admin.site.register(Power)
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
