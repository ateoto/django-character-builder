$(function() {
	$('#standard-array-abilities').sortable({
		update: function(event, ui) {
			var order = $(this).sortable('toArray');
			for (var i = 0; i < order.length; i++)
			{
				$('#' + order[i] + ' > .badge').text(standard_array[i]);
			}
		}
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
	$('#btn-personal').click(function() {
		$('#info > *').hide();
		$('#builder-ux > *').hide();
		$('#personal').show();
	});
	$('#btn-abilities').click(function() {
		$('#info > *').hide();
		$('#builder-ux > *').hide();
		$('#abilities').show();
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

var standard_array = [16, 14, 13, 12, 11, 10];

function ability_modifer(ability_value) {
	return Math.floor((Math.abs(ability_value) - 10) / 2)
}