$(function() {

	$.ajaxSetup({ 
	     beforeSend: function(xhr, settings) {
	         function getCookie(name) {
	             var cookieValue = null;
	             if (document.cookie && document.cookie != '') {
	                 var cookies = document.cookie.split(';');
	                 for (var i = 0; i < cookies.length; i++) {
	                     var cookie = jQuery.trim(cookies[i]);
	                     // Does this cookie string begin with the name we want?
	                 if (cookie.substring(0, name.length + 1) == (name + '=')) {
	                     cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
	                     break;
	                 }
	             }
	         }
	         return cookieValue;
	         }
	         if (!(/^http:.*/.test(settings.url) || /^https:.*/.test(settings.url))) {
	             // Only send the token to relative URLs i.e. locally.
	             xhr.setRequestHeader("X-CSRFToken", getCookie('csrftoken'));
	         }
	     } 
	});

	my_character = CharacterBuilder.character;

	$('#info > *').hide();

	$('.std-arr-ability').popover(options = {trigger: 'hover'}	);

	$('#standard-array-abilities').sortable({
		start: function(event, ui) {
			$('.std-arr-ability').popover('hide');
		},
		update: function(event, ui) {
			update_abilities();
			save_abilities();	
		},
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
		update_personal();
		save_personal();
		update_abilities();
		save_abilities();
		$('#info > *').hide();
		$('#builder-ux > *').hide();
		$('#personal').show();
	});

	$('#btn-abilities').click(function() {
		update_personal();
		save_personal();
		update_abilities();
		save_abilities();
		$('#info > *').hide();
		$('#builder-ux > *').hide();
		$('#abilities').show();
		$('#ability-info').show();
	});

	$('#btn-skills').click(function() {
		update_personal();
		save_personal();
		update_abilities();
		save_abilities();
		$('#info > *').hide();
		$('#builder-ux > *').hide();
		$('#skills').show();
	});

	$('#btn-powers').click(function() {
		update_personal();
		save_personal();
		update_abilities();
		save_abilities();
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
	for (var i = 0; i < order.length; i++) {
		var ability_name = $('#' + order[i] + ' .ability-text').text().toLowerCase();
		var ability_value = CharacterBuilder.standard_array[i];
		my_character[ability_name] = ability_value;
		$('#' + order[i] + ' > .badge').text(CharacterBuilder.standard_array[i]);
	}
	my_character.abilities = abilities;
	$('#id_character').val(my_character.character_id);
 	$('#id_strength').val(my_character.strength);
 	$('#id_constitution').val(my_character.constitution);
 	$('#id_dexterity').val(my_character.dexterity);
 	$('#id_intelligence').val(my_character.intelligence);
 	$('#id_wisdom').val(my_character.wisdom);
 	$('#id_charisma').val(my_character.charisma);
}

function save_personal() {
	$('#personal-form .control-group').removeClass('error');
	if (!my_character.submitted) {
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
	    			$('#info > *').hide();
					$('#builder-ux > *').hide();
					$('#personal').show();
	    		}
	  	}, "json");
	}
}

function save_abilities() {
	if (my_character.submitted) {
		$.post($('#ability-form').attr('action'), $('#ability-form').serialize(),
			function(data) {
				if (!data.valid) {
					console.log(data.errors);
				}
		}, "json");
	}
}
