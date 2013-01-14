$(function() {
	$('#id_race').change(function(){
		race_id = $('#id_race').val();
		$('#info > *').hide();
		$('#race-' + race_id).show();
	});
	$('#id_class_type').change(function(){
		class_type_id = $('#id_class_type').val();
		$('#info > *').hide();
		$('#classtype-' + class_type_id).show();
	});
});