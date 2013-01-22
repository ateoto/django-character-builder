var CharacterBuilder = {
	character: {
		submitted: false,
		character_id: null,
		name: null,
		race: null,
		class_type: null,
		alignment: null,
		deity: null,
		height: null,
		weight: null,
		age: null,
		abilities: [],
	},
	standard_array : [16, 14, 13, 12, 11, 10],
};

CharacterBuilder.half_level = function(level) {
	return Math.floor(level / 2);
}

CharacterBuilder.ability_modifer = function(ability_value) {
	return Math.floor((Math.abs(ability_value) - 10) / 2);
}

CharacterBuilder.pretty_mod = function(modifier) {
	if (modifier < 0) {
		prepend = '-';
	} else if (modifier > 0) {
		prepend = '+';
	} else {
		prepend = '';
	}
	return prepend + modifier.toString();
}