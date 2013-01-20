from django import forms
from django.forms import ModelForm
from character_builder.models import Character

from crispy_forms.helper import FormHelper


class CharacterFormUser(ModelForm):
    def __init__(self, *args, **kwargs):
        super(CharacterFormUser, self).__init__(*args, **kwargs)
        self.helper = FormHelper(self)
        self.helper.form_id = "personal-form"
        self.helper.form_action = "character-builder-save-personal"
        #self.helper.form_class = 'form-horizontal'

    class Meta:
        model = Character
        fields = ('name', 'race', 'gender', 'class_type', 'alignment', 'deity',
                    'height', 'weight', 'age')


class CharacterAbilityForm(forms.Form):
    character = forms.IntegerField(widget=forms.HiddenInput())
    strength = forms.IntegerField(widget=forms.HiddenInput())
    constitution = forms.IntegerField(widget=forms.HiddenInput())
    dexterity = forms.IntegerField(widget=forms.HiddenInput())
    intelligence = forms.IntegerField(widget=forms.HiddenInput())
    wisdom = forms.IntegerField(widget=forms.HiddenInput())
    charisma = forms.IntegerField(widget=forms.HiddenInput())

    def __init__(self, *args, **kwargs):
        super(CharacterAbilityForm, self).__init__(*args, **kwargs)
        self.helper = FormHelper(self)
        self.helper.form_id = "ability-form"
        self.helper.form_action = "character-builder-save-abilities"
