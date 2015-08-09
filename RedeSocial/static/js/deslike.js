// ---------------- 1: deslike postagem normal -------------------
$(document).on("click", ".deslike", function() {
	var li = $(this).closest(".containerPostagem");
	var hide_deslike = $("#hide", li).val();

	$.ajax({
		url : 'despingo',
		data : {
			'cID_post' : hide_deslike,
		},
		type : 'post',
		cache : false,
		success : function(data) {
			$(".u-curtidas", li).val("(" + data + ")");
			$(".deslike img", li).attr("src", "../static/imagens/despingo.png");
			$(".deslike", li).attr("class", "like");
		}

	});
	return false;
});//1: fim like postagem normal ---------------------------------

//---------------- 2: deslike postagem desafio -------------------
$(document).on("click", ".deslike-desafio", function() {
	var li = $(this).closest(".containerPostagemDesafio");
	var hide_deslike = $("#hide", li).val();

	$.ajax({
		url : 'despingo',
		data : {
			'cID_post' : hide_deslike,
		},
		type : 'post',
		cache : false,
		success : function(data) {
			$(".u-curtidas", li).val("(" + data + ")");
			$(".deslike-desafio img", li).attr("src", "../static/imagens/despingo.png");
			$(".deslike-desafio", li).attr("class", "like-desafio");
		}

	});
	return false;
});//2: fim deslike postagem desafio ------------------------------------------