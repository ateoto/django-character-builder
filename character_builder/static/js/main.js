$(function() {
	$('#info > *').hide();

	$('.std-arr-ability').popover(options = {trigger: 'hover'}	);

	$('#standard-array-abilities').sortable({
		start: function(event, ui) {
			$('.std-arr-ability').popover('hide');
		},
		update: function(event, ui) {
			var order = $(this).sortable('toArray');
			for (var i = 0; i < order.length; i++)
			{
				$('#' + order[i] + ' > .badge').text(CharacterBuilder.standard_array[i]);
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
		$('#info > *').hide();
		$('#builder-ux > *').hide();
		$('#abilities').show();
		$('#ability-info').show();

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
