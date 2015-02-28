$(document).ready(function(){
	$('#id_privacy').on('change', function () {
		if(this.value === "3"){
			$("#allowed").show();
		} else {
			$("#allowed").hide();
		}	
	});
});