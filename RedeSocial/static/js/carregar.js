$(document).ready(function() {
// 1: -------------- Ver mais feeds ----------------
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
	});// 1: fim

// -------------- 2: se o input file do post mudar -----------
	$(document).on("change", "#arquivo", function(){
	
		$("#btn-publicar").removeClass("disabled");
		$("#btn-publicar").removeAttr("disabled", "disabled");
		
	}); // 2: fim
	
// -------------- 3: se digitar alguma coisa no campo de texto do post ---------
	$(document).on("keyup", "#text-post", function(){
		
		$("#btn-publicar").removeClass("disabled");
		$("#btn-publicar").removeAttr("disabled", "disabled");
		
		var valor = $("#text-post").val();
		var valor2 = $("#arquivo").val();
		
		if(valor == "" && valor2 == ""){
			$("#btn-publicar").addClass("disabled");
			$("#btn-publicar").attr("disabled", "disabled");
		}
		
	}); // 3: fim

//------------- 4: publica a postagem ----------------
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
	});// 4: fim
});// fim document ready

// ------------ 5: quando clica em desafiar amigo direciona pra tela desafiar -------
$(document).on("click", "#btn-desafiar", function(){
	var id = $("#hide-desafio").val();
	
	$.ajax({
		url: 'desafiar_amigo',
		data : {
			'id_usuario' : id,
		},
		type: "post",
		cache : false,
		success: function(data){
			
			$("#containerFeedGeral").empty();
			$("#containerFeedGeral").append(data);
		}
		
	});
	return false;
});// 5: fim

//--------------- 6: lança um desafio ao amigo -------------//
$(document).on("click", "#btn-lancar", function(){
	var id_desafio = $("option:selected").val();
	var id_amigo = $("#hide-amigo").val();
	
	$.ajax({
		url: 'lancar_desafios',
		data : {
			'cDesafios' : id_desafio,
			'cAmigos' : id_amigo,
		},
		type: "post",
		cache : false,
		success: function(data){
			
			alert(data);
		}
		
	});
	return false;
});// 6: fim

//-------------- 7: aceita os desafios pendentes ------------------
$(document).on("click", ".btn-aceitar", function(){
	var ul = $(this).closest(".pendentes");

	var id_usuario = $("#hide-id-usuario", ul).val();
	var id_desafio = $("#hide-id-desafio", ul).val();
	var id_pedido = $("#hide-id-pedido", ul).val();
	var id_solicitacao = $("#hide-id-solicitacao", ul).val();
	
	$.ajax({
		url: "pedido_desafio",
		type: "post",
		data: {
			'cPedido_solicitacao' : id_solicitacao,
			'cPedido_usuario_id' : id_usuario,
			'cPedido_desafio_id' : id_desafio,
			'cPedido_id' : id_pedido,
		},
		success: function(data){
	
			
			//, qtd_soli_desafios, qtd_d_ativos_desafiado
			//$("#badge-pendentes").remove();
			$(ul).hide('slide', {direction: 'left'}, 500, function(){
				$(ul).remove(); 
			});
			
			/*$(ul).slideUp(500, function() { 
				$(ul).remove(); 
			});*/
			
			$(".notificacoes-desafios").load("timeline .ul-desafios");
		
			//$("#badge-ativos").val(qtd_d_ativos_desafiado);
		}
	});
	return false;
});// 7: fim

// --------------- 8: recusa desafio pendente -----------------
$(document).on("click", ".btn-recusar", function(){
	var ul = $(this).closest(".pendentes");

	var id_usuario = $("#hide-id-usuario-recusar", ul).val();
	var id_desafio = $("#hide-id-desafio-recusar", ul).val();
	var id_pedido = $("#hide-id-pedido-recusar", ul).val();
	var id_solicitacao = $("#hide-id-solicitacao-recusar", ul).val();
	
	$.ajax({
		url: "pedido_desafio",
		type: "post",
		data: {
			'cPedido_solicitacao' : id_solicitacao,
			'cPedido_usuario_id' : id_usuario,
			'cPedido_desafio_id' : id_desafio,
			'cPedido_id' : id_pedido,
		},
		success: function(data){
	
			
			//, qtd_soli_desafios, qtd_d_ativos_desafiado
			//$("#badge-pendentes").remove();
			$(ul).hide('slide', {direction: 'left'}, 500, function(){
				$(ul).remove(); 
			});
			
			/*$(ul).slideUp(500, function() { 
				$(ul).remove(); 
			});*/
			
			$(".notificacoes-desafios").load("timeline .ul-desafios");
		
			//$("#badge-ativos").val(qtd_d_ativos_desafiado);
		}
	});
	return false;
});// 8: fim

//--------------- 9: remove msg -----------------
$(document).on("submit", "#form-remove-msg", function(){
	var container = $(this).closest(".container-mensagem-remove");

	$.ajax({
		url: "apagar_mensagem",
		type: "post",
		data: $("#form-remove-msg").serialize(),
		success: function(data){
	
			
			//, qtd_soli_desafios, qtd_d_ativos_desafiado
			//$("#badge-pendentes").remove();
			$(container).hide('slide', {direction: 'left'}, 500, function(){
				$(container).remove(); 
			});
			
			/*$(ul).slideUp(500, function() { 
				$(ul).remove(); 
			});*/
			
			$(".notificacoes-msg").load("timeline .ul-msg");
		
			//$("#badge-ativos").val(qtd_d_ativos_desafiado);
		}
	});
	return false;
});// 9: fim

//--------------- 9: remove msg -----------------
$(document).on("submit", "#form-aceitar-solicitacao", function(){
	var ul = $(this).closest("#ul-solicitacoes");

	$.ajax({
		url: "pedido_Solicitacao",
		type: "post",
		data: $("#form-aceitar-solicitacao").serialize(),
		success: function(data){
	
			
			//, qtd_soli_desafios, qtd_d_ativos_desafiado
			//$("#badge-pendentes").remove();
			$(ul).hide('slide', {direction: 'left'}, 500, function(){
				$(ul).remove(); 
			});
			
			/*$(ul).slideUp(500, function() { 
				$(ul).remove(); 
			});*/
			$("#ul-amigos").empty();
			$("#ul-amigos").load("amigos #ul-amigos");
		
			//$("#badge-ativos").val(qtd_d_ativos_desafiado);
		}
	});
	return false;
});// 9: fim