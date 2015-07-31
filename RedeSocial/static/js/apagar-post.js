$(document).ready(function(){
	$("#idapagar{{ forloop.counter }}").live("submit", function() {
		
		var url = "apagar_postagem"; // the script where you handle the form input.
		
			$.ajax({
				type: "POST",
				url: url,
				data: $("#idapagar{{ forloop.counter }}").serialize(), // serializes the form's elements.
				success: function(data)
				{
					// show response from the php script.
					$("#containerPostagem").remove();
				}
			});
		
		return false; // avoid to execute the actual submit of the form.
	});
});