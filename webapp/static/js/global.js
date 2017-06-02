$(document).ready(function() {

	$("#rating tbody tr").on('click touch', function(e){
		var shooterId = $(e.currentTarget).data('shooter_id');
		window.location.href = "/shooter/?shooter_id=" + shooterId;
	});

	$("#competitions tbody tr").on('click touch', function(e){
		var competitionId = $(e.currentTarget).data('competition_id');
		window.location.href = "/match/?match_id=" + competitionId;
	});

	$("#shooters tbody tr").on('click touch', function(e){
		var shooterId = $(e.currentTarget).data('shooter_id');
		window.location.href = "/shooter/?shooter_id=" + shooterId;
	});

});
