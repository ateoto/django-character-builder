from django.contrib import admin

from character_builder.models import Source, Race, Role, Skill, Ability, CharacterSkill, CharacterAbility, ClassType, Character, Size

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
admin.site.register(Character)
