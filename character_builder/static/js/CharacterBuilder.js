var CharacterBuilder = {}

CharacterBuilder.standard_array = [16, 14, 13, 12, 11, 10];

CharacterBuilder.ability_modifer = function(ability_value) {
	return Math.floor((Math.abs(ability_value) - 10) / 2);
}