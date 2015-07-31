$(document).on("click", ".deslike", function() {
	var li = $(this).closest(".containerPostagem");
	var feed = $(li).attr("id");
	var hii = $("#hide", li).val();

	$.ajax({
		url : 'despingo',
		data : {
			'cID_post' : feed,
			'hii' : hii
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
});