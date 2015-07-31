$(document).on("click", ".like", function() {
	var li = $(this).closest(".containerPostagem");
	var feed = $(li).attr("id");
	var hii = $("#hide", li).val();

	$.ajax({
		url : 'pingo',
		data : {
			'cID_post' : feed,
			'hii' : hii
		},
		type : 'post',
		cache : false,
		success : function(data) {
			$(".u-curtidas", li).val("(" + data + ")");
			$(".like img", li).attr("src", "../static/imagens/pingo.png");
			$(".like", li).attr("class", "deslike");
		
		}

	});
	return false;
});

$(document).on("submit", "#postar-comentario", function() {
	var li = $(this).closest(".containerPostagem");
	var feed = $(li).attr("id");
	var hi = $(".formTextAreaTimeLine", li).val();

	$.ajax({
		url : 'postarComentarios',
		data : {
			'cId' : feed,
			'cComentario': hi,
		},
		type : 'post',
		cache : false,
		success : function(data) {
			$(".linkPostagem", li).val("Comentários (" + data + ")");
			$(".formTextAreaTimeLine", li).val('');
		
		}

	});
	return false;
});

$(document).on('submit', '#id-apagar', function() {
	var li = $(this).closest(".containerPostagem");
	var feed = $(li).attr("id");
	
    var url = "apagar_postagem"; // the script where you handle the form input.

    $.ajax({
           type: "POST",
           url: url,
           data : {
   			'id' : feed,
   			}, // serializes the form's elements.
           success: function(data)
           {
               // show response from the php script.
               $(li).remove();
           }
         });

    return false; // avoid to execute the actual submit of the form.
});