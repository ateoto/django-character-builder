$(function() {
	my_character = CharacterBuilder.character;

	$('#info > *').hide();

	$('.std-arr-ability').popover(options = {trigger: 'hover'}	);

	$('#standard-array-abilities').sortable({
		start: function(event, ui) {
			$('.std-arr-ability').popover('hide');
		},
		update: update_abilities,
	});

	$('#standard-array-abilities').disableSelection();

	$('#id_race').change(function() {
		race_id = $('#id_race').val();
		$('#info > *').hide();
		$('#race-' + race_id).show();
	});

	$('#id_class_type').change(function() {
		class_type_id = $('#id_class_type').val();
		$('#info > *').hide();
		$('#classtype-' + class_type_id).show();
	});

	$('#id_deity').change(function() {
		deity_id = $('#id_deity').val();
		$('#info > *').hide();
		$('#deity-' + deity_id).show();
	});

	$('#btn-personal').click(function() {
		$('#info > *').hide();
		$('#builder-ux > *').hide();
		$('#personal').show();
	});

	$('#btn-abilities').click(function() {
		update_personal();
		if (!my_character.submitted) {
			save_personal();

		} else {
			$('#info > *').hide();
			$('#builder-ux > *').hide();
			update_abilities();
			$('#abilities').show();
			$('#ability-info').show();
		}
	});

	$('#btn-skills').click(function() {
		$('#info > *').hide();
		$('#builder-ux > *').hide();
		$('#skills').show();
	});

	$('#btn-powers').click(function() {
		$('#info > *').hide();
		$('#builder-ux > *').hide();
		$('#powers').show();
	}); 
});

function update_personal() {
	var new_personal = $('#personal-form').serializeArray();
	$.each(new_personal, function(index, value){
		if (value.value !== '') {
			my_character[value.name] = value.value;
		}
	});
}	

function update_abilities() {
	var order = $('#standard-array-abilities').sortable('toArray');
	console.log(order);
	for (var i = 0; i < order.length; i++) {
		$('#' + order[i] + ' > .badge').text(CharacterBuilder.standard_array[i]);
	}
}

function save_personal() {
	$('#personal-form .control-group').removeClass('error');
	$.post($('#personal-form').attr('action'), $('#personal-form').serialize(),
  		function(data){
  			if (data.valid) {
    			my_character.character_id = data.character_id; 
    			my_character.submitted = true;
    		} else {
    			console.log('There were errors.');
    			$.each(data.errors, function(i, value) {
    				$('#div_id_' + i).addClass('error');
    			});
    		}
  	}, "json");
}

function save_abilities() {

}