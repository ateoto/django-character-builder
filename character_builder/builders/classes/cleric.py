from character_builder.models import Character, CharacterAbility, CharacterSkill

"""
This is where I come up with some sort of API to perform all the 
customization during a character build.
"""

def class_abilities(character):
	"""
	The character object, by the time it gets here should have it's base numbers, class, and race.
	"""


def hit_points(character):
	"""
	Clerics get 12 + Con at level one
	"""

	abilities = CharacterAbility.objects.filter(character=character)
	con = abilities.get(ability__name="Constitution")
	character.hit_points = 12 + con.value
	# Should I set this here, or return it to whatever called this function?