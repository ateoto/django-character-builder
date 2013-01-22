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
	var my_character = get_character();
});

function get_character() {
	var character_data;
	$.post($('#character-getter').attr('action'), $('#character-getter').serialize(),
		function(data){
			character_data = data.character;
			update_ability_scores(character_data);
	}, "json");
	return character_data;
}

function update_ability_scores(character_data) {
	$('.ability-score').each(function(index){
		var element_id = $(this).attr('id');
		var value = parseInt($('.ability-value', this).text(), 10);
		var modifier = CharacterBuilder.ability_modifer(value);
		if (modifier < 0)
		{
			prepend = '-';
		} else if (modifier === 0) {
			prepend = '';
		} else {
			prepend = '+';
		}
		$('.ability-mod', this).text(prepend + modifier);

		// This is how we should actually work:
		$('.ability-mod-level', this).text(modifier + CharacterBuilder.half_level(character_data.level))
	});
}