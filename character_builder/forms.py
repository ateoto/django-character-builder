from django.forms import ModelForm
from character_builder.models import Character

from crispy_forms.helper import FormHelper


class CharacterFormUser(ModelForm):
    def __init__(self, *args, **kwargs):
        super(CharacterFormUser, self).__init__(*args, **kwargs)
        self.helper = FormHelper(self)
        self.helper.form_id = "personal-form"
        self.helper.form_action = "character-builder-save"
        #self.helper.form_class = 'form-horizontal'

    class Meta:
        model = Character
        fields = ('name', 'race', 'class_type', 'alignment', 'deity',
                    'height', 'weight', 'age')
