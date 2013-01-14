from django.forms import ModelForm, ModelChoiceField, Select
from character_builder.models import Character


class CharacterFormStepOne(ModelForm):
    class Meta:
        model = Character
        fields = ('name', 'class_type', 'race')


class CharacterFormUser(ModelForm):
    class Meta:
        model = Character
        fields = ('name', 'race', 'class_type', 'alignment', 'deity',
                    'height', 'weight', 'age')


class CharacterFormPersonal(ModelForm):
    class Meta:
        model = Character
        fields = ('name', 'weight', 'age', 'deity', 'alignment')
