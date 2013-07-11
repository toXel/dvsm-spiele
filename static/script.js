$(document).ready(function(){
	$(".toggle").click( function() {
		$(".edit").toggle();
		$(".open").toggle();
		$(".close").toggle();
	});
	setTimeout(function() {
    $(".flash").slideUp("fast");
}, 3000);
});