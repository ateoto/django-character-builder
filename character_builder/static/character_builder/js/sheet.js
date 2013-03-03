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
	update_character(character_id);
	setInterval(update_health, 5000, character_id);
	setInterval(update_character, 60000, character_id);

	$('#powers').hide();
	$('#notes').hide();

    $('#nav-stats-link').click(function() {
    	$('#side-nav > .active').removeClass('active');
    	$(this).addClass('active');
    	$('#character-stats').show();
		$('#powers').hide();
		$('#notes').show();

		return false; 	
    });

    $('#nav-def-link').click(function() {
    	$('#side-nav > .active').removeClass('active');
    	$(this).addClass('active');
    	$('#character-stats').show();
		$('#powers').hide();
		$('#notes').show();

		return false;
    });

    $('#nav-abilities-link').click(function() {
    	$('#side-nav > .active').removeClass('active');
    	$(this).addClass('active');
    	$('#character-stats').show();
		$('#powers').hide();
		$('#notes').show();    	

		return false;
    });

    $('#nav-skills-link').click(function() {
    	$('#side-nav > .active').removeClass('active');
    	$(this).addClass('active');
    	$('#character-stats').show();
		$('#powers').hide();
		$('#notes').show();

		return false;
    });

	$('#nav-notes-link').click(function() { 
		$('#side-nav > .active').removeClass('active');
		$(this).addClass('active');
		$('#character-stats').hide();
		$('#powers').hide();
		$('#notes').show();

		return false;
	});

	$('#nav-powers-link').click(function() {
		$('#side-nav > .active').removeClass('active');
		$(this).addClass('active');
		$('#character-stats').hide();
		$('#powers').show();
		$('#notes').hide();

		return false;
	});

	$('#character-notes').on('focusout', save_notes);

});

function test_tasty(cid) {
	$.get('/DnD/api/v1/character/' + cid + '/','',
		function(data) {
			console.log(data);
	}, "json");
}

function update_character(character_id) {
	$.get('/DnD/api/v1/character/' + character_id + '/', '',
		function(data) {
			update_ability_scores(data);
			update_xp(data);
			update_hp(data);
		}, "json");
}

function update_health(character_id) {
	$.get('/DnD/api/v1/character_health/' + character_id + '/', '',
		function(data) {
			update_hp(data);
		}, "json");
}

function update_ability_scores(character_data) {
	_.each(character_data.abilities, function(element) {
		$('#ability-score-' + element.name + ' .ability-mod-level').text(element.modifier_half_level);
	});
}

function update_xp(character_data) {
	$('#level-text').text(character_data.level);
	$('#xp-text').text(character_data.xp);
	$('#next-level-xp-text').text(character_data.next_level_xp_needed);
	var xp_percentage = (character_data.xp - character_data.level_xp_needed) / (character_data.next_level_xp_needed - character_data.level_xp_needed) * 100;
	$('#xp-bar').css("width", xp_percentage + "%");
}

function update_hp(character_data) {
	var hp_percentage = ((character_data.hit_points / character_data.max_hit_points) * 100);
	$('#hit-points').text(character_data.hit_points);

	if (hp_percentage <= 30) {
		console.log('Danger');
		$('#health-bar-parent').removeClass("progress-success progress-warning").addClass("progress-danger");
	}
	else if (hp_percentage > 30 && hp_percentage <= 50) {
		console.log('Warning');
		$('#health-bar-parent').removeClass("progress-success progress-danger").addClass("progress-warning");
	}
	else {
		console.log('Success');
		$('#health-bar-parent').removeClass("progress-warning progress-danger").addClass("progress-success");
	}
	$('#health-bar').css("width", hp_percentage + "%");
}

function save_notes() {
	var cid = $('#character-notes').attr('character-id');
	var notes = $('#character-notes').val();

	var resource_uri = '/DnD/api/v1/character/' + cid + '/';
	
	console.log(resource_uri);
	
	$.ajax({
		url: resource_uri,
		type: 'PATCH',
		contentType: 'application/json',
		data: JSON.stringify({ "notes": notes }),
		dataType: 'json',
		processData: false,
        beforeSend: function(jqXHR, settings) {
        	jqXHR.setRequestHeader('X-CSRFToken', $('input[name=csrfmiddlewaretoken]').val());
        },
        success: function(data, textStatus, jqXHR) {
        	console.log('Right on.');
        },
	});
}
