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

CharacterBuilder.ability_modifer = function(ability_value) {
	return Math.floor((Math.abs(ability_value) - 10) / 2);
}
