/*
*Hides the Custom choose bar until Custom is choosen from privacy
*/
$(document).ready(function(){
	$('#id_privacy').on('change', function () {
		if(this.value === "3"){
			$("#allowed").show();
		} else {
			$("#allowed").hide();
		}	
	});
});
/*
*Removes admin from a selection of usernames
*/
$(document).ready(function(){
	$("#id_allowed option[value='1']").remove();
});