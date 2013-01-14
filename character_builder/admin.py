from django.contrib import admin
from character_builder.models import (Source, Race, Role, Skill, Ability,
                                    CharacterSkill, CharacterAbility,
                                    ClassType, Character, Size,
                                    PowerType, Power, Language,
                                    RaceAbilityMod, RaceSkillMod,
                                    Alignment, Deity)


class ClassTypeAdmin(admin.ModelAdmin):
    list_display = ('name', 'role', 'source')

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
