$(document).ready(function() {
	$(document).on('submit', "#verMais", function() {
		$("#verMais").hide();
		$(".sk-circle").show();

		$.ajax({
			type : "POST",
			url : "mais_posts",
			data : $("#verMais").serialize(),// serializes the form's elements.
			success : function(data) {
				// show response from the php script.
				$("#containerFeed2").append(data);

			},
			complete: function () {
		          $(".sk-circle").hide();
		          $("#verMais").remove();
			}
		});
		return false;
	});
	
	$(document).on("change", "#arquivo", function(){
	
		$("#btn-publicar").removeClass("disabled");
		$("#btn-publicar").removeAttr("disabled", "disabled");
		
	});
	
	$(document).on("keyup", "#text-post", function(){
		
		$("#btn-publicar").removeClass("disabled");
		$("#btn-publicar").removeAttr("disabled", "disabled");
		
		var valor = $("#text-post").val();
		var valor2 = $("#arquivo").val();
		
		if(valor == "" && valor2 == ""){
			$("#btn-publicar").addClass("disabled");
			$("#btn-publicar").attr("disabled", "disabled");
		}
		
	});
	
	$(document).on('submit', '#idpostar', function(e) {
		
		$.ajax({
			url : 'postar',
			type : 'POST',
			data : new FormData(this),
			processData : false,
			contentType : false,
			success : function(data) {
				// show response from the php script.
				$("#containerFeed2").load("feed");
				$("#text-post").val('');
				$("#arquivo").val('');
				$("#btn-publicar").addClass("disabled");
				$("#btn-publicar").attr("disabled", "disabled");
			}
		});
		
		e.preventDefault();
	});
});


