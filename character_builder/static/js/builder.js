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

	$('.std-arr-ability').popover(options = {trigger: 'hover'}	);

	$('#standard-array-abilities').sortable({
		create: function(event, ui) {
			update_abilities();
		},
		start: function(event, ui) {
			$('.std-arr-ability').popover('hide');
		},
		update: function(event, ui) {
			update_abilities();
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

	$('.human-bonus').click(function() {
		var bonus_ability_name = $(this).text().toLowerCase();	
		var bonus_element = $('.human-bonus-dom', this).html();
		$('#racial-ability-bonus-list').empty();
		$('#racial-ability-bonus-list').append(bonus_element);

		$('.human-bonus').removeClass('active');
		$(this).addClass('active');

		update_abilities();
	});



	$('#id_race').change();
});

function get_class_bonuses(class_type_id) {

}
function get_racial_bonuses(race_id) {

}

function update_abilities() {
	var bonuses = [];
	$('#racial-ability-bonus-list .racial-ability-bonus').each(function(index) {
		var bonus_ability_name = $('.ability-text', this).text().toLowerCase();
		var bonus_ability_modifier = parseInt($('.ability-modifier', this).text(), 10);
		bonuses.push({ 
			'name': bonus_ability_name, 
			'modifier': bonus_ability_modifier
		});
	});

	var order = $('#standard-array-abilities').sortable('toArray');
	for (var i = 0, len = order.length; i < len; i++) {
		var ability_name = $('#' + order[i] + ' .ability-text').text().toLowerCase();
		var ability_value = CharacterBuilder.standard_array[i];
		for (j = 0, blen = bonuses.length; j < blen; j++) {
			if (ability_name === bonuses[j].name) {
				ability_value += bonuses[j].modifier;
			}
		}
		my_character[ability_name] = ability_value;
		$('#' + order[i] + ' > .badge').text(ability_value);
	}
	my_character.abilities = abilities;
 	$('#id_strength').val(my_character.strength);
 	$('#id_constitution').val(my_character.constitution);
 	$('#id_dexterity').val(my_character.dexterity);
 	$('#id_intelligence').val(my_character.intelligence);
 	$('#id_wisdom').val(my_character.wisdom);
 	$('#id_charisma').val(my_character.charisma);
}