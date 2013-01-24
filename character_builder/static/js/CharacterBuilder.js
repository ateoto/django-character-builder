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
		racial_ability_bonues: [],
	},
	standard_array : [16, 14, 13, 12, 11, 10],
};

CharacterBuilder.get_character = function() {
	var character_data;
	$.post($('#character-getter').attr('action'), $('#character-getter').serialize(),
		function(data){
			character_data = data.character;
	}, "json");
	console.log(this.character_id);
	console.log(character_data.character_id);
	return character_data;
}

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