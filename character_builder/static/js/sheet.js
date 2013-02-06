$(function() {
	$('#character-getter').hide();

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
	var my_character = get_character(character_id);
	setInterval(update_character, 10000, character_id);
});




function test_tasty(cid) {
	$.get('/DnD/api/v1/character/' + cid + '/','',
		function(data) {
			console.log(data);
	}, "json");
}


function get_character(character_id) {
	var character_data;
	$.get('/DnD/api/v1/character/' + character_id + '/','',
		function(data){
			character_data = data
			update_ability_scores(character_data);
	}, "json");
	return character_data;
}

function update_character(character_id) {
	$.get('/DnD/api/v1/character/' + character_id + '/', '',
		function(data) {
			update_ability_scores(data);
			update_xp(data);
		}, "json");
}


function update_ability_scores(character_data) {
	_.each(character_data.abilities, function(element) {
		$('#ability-score-' + element.ability.name + ' .ability-mod').text(element.modifier);
		$('#ability-score-' + element.ability.name + ' .ability-mod-level').text(element.modifier_half_level);
	});
}

function update_xp(character_data) {
	$('#level-text').text(character_data.level);
	$('#xp-text').text(character_data.xp);
	$('#next-level-xp-text').text(character_data.next_level_xp_needed);
	1000
	2250
	2250-1000
	var xp_percentage = (character_data.xp - character_data.level_xp_needed) / (character_data.next_level_xp_needed - character_data.level_xp_needed) * 100;
	$('#xp-bar').css("width", xp_percentage + "%");
}