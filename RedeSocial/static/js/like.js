// ---------------- 1: like postagem normal -------------------
$(document).on("click", ".like", function() {
	var li = $(this).closest(".containerPostagem");
	var hide_like = $("#hide", li).val();

	$.ajax({
		url : 'pingo',
		data : {
			'cID_post' : hide_like,
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
});//1: fim like postagem normal ------------------------------

//---------------- 2: like postagem desafio -------------------
$(document).on("click", ".like-desafio", function() {
	var li = $(this).closest(".containerPostagemDesafio");
	var hide_like = $("#hide", li).val();

	$.ajax({
		url : 'pingo',
		data : {
			'cID_post' : hide_like,
		},
		type : 'post',
		cache : false,
		success : function(data) {
			$(".u-curtidas", li).val("(" + data + ")");
			$(".like-desafio img", li).attr("src", "../static/imagens/pingo.png");
			$(".like-desafio", li).attr("class", "deslike-desafio");
		
		}

	});
	return false;
});//2: fim like postagem desafio -----------------------------

//3: ------------- postar comentario na postagem normal --------------------
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
});//3: fim ------------- postar comentario na postagem normal --------------

//4: ------------- postar comentario na postagem desafio --------------
$(document).on("submit", "#postar-comentario-desafio", function() {
	var li = $(this).closest(".containerPostagemDesafio");
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
});//4: fim ------------- postar comentario na postagem desafio --------------

//5: ------------- apagar postagem normal ------------------------------------
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
           success: function(data){
               
        	   $(li).fadeOut(300, function(){
            	   $(li).remove();
               });
           	}
         });

    return false; // avoid to execute the actual submit of the form.
});//5: fim ------- apagar postagem normal ------------------------------------

//6: ------------- apagar postagem desafio------------------------------------
$(document).on('submit', '#id-apagar-desafio', function() {
	var li = $(this).closest(".containerPostagemDesafio");
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
        	   $(li).fadeOut(300, function(){
            	   $(li).remove();
               });
           }
         });

    return false; // avoid to execute the actual submit of the form.
});//5: fim ------- apagar postagem desafio ------------------------------------

//6: ------------- apagar comentario de uma postagem normal ------------------------------------
$(document).on('submit', '#id-apagar-comentario', function() {
	var container = $(this).closest("#li-comentarios");
	
	var hide_comentario_id = $("#hide-comentario-id", container).val();
	var hide_comentario_postagem = $("#hide-comentario-postagem", container).val();
	
    var url = "apagar_comentario"; // the script where you handle the form input.

    $.ajax({
           type: "POST",
           url: url,
           data : {
   			'id' : hide_comentario_id,
   			'id_postagem' : hide_comentario_postagem,
   			}, // serializes the form's elements.
           success: function(data){
               
        	   $(container).fadeOut(300, function(){
            	   $(container).remove();
               });
           	}
         });

    return false; // avoid to execute the actual submit of the form.
});//6: fim ------- apagar postagem normal ------------------------------------