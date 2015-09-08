$(document).ready(function() {
//  -------------- Modal usuarios curtiram Postagem Normal ----------------	
	$(document).on("click", "#abrir-modal", function(){
		var li = $(this).closest(".containerPostagem");
		
		var action = $(this).attr("action");
		   
		var modal = $("#wrap-modal");
		   
		var alturaTela = $(document).height();
	    var larguraTela = $(window).width();
	     
	       //colocando o fundo preto
	    $('#mascara').css({'width':larguraTela,'height':alturaTela});
	    $('#mascara').fadeIn(300); 
	    $('#mascara').fadeTo("slow",0.5);
	    
	    var scroll = $(document).scrollTop() + 150;
	    
	    var left = ($(window).width() /2) - ( $(modal).width() / 2 );
	    var top = ($(window).height() / 2) - ( $(modal).height() / 2 );
	     
	    $(modal).css({'top':scroll,'left':left});
		$(modal).show();
		
		$("#loader-curtiram").show();
		
		$("body").css("overflow", "hidden");
		
		var content = $("#recebe-modal");
		
		window.setTimeout( function(){   
		$.ajax({
			url: action,
			type : "POST",
			data : $("#abrir-modal", li).serialize(),
			cache: false,
			success: function( response ){
				var data = $( '<div>'+response+'</div>' ).find('#wrap-modal-curtiram').html();
				$("#loader-curtiram").hide();	
				content.html( data ).hide();
				content.html( data ).show();
				   
			}
	   });
		}, 1000);
	   return false;
	});
	   
	   $(document).on("click", "#mascara", function(){
		   $(this).hide();
	       $("#wrap-modal").hide();
	       $("#recebe-modal").empty();
	       $("body").css("overflow", "auto");
	   });
	   
	   $(document).on("click", ".close", function(){
		   $("#wrap-modal").hide();
		   $('#mascara').hide();
		   $("#recebe-modal").empty();
		   $("body").css("overflow", "auto");
	   });
	   
//FIM:  -------------- Modal usuarios curtiram Postagem Normal ----------------
	   
	   
//  -------------- Modal usuarios curtiram Postagem Desafio ----------------	
	$(document).on("click", "#abrir-modal-desafio", function(){
		var li = $(this).closest(".containerPostagemDesafio");
			
		var action = $(this).attr("action");
			   
		var modal = $("#wrap-modal");
			   
		var alturaTela = $(document).height();
		var larguraTela = $(window).width();
		     
		       //colocando o fundo preto
	    $('#mascara').css({'width':larguraTela,'height':alturaTela});
	    $('#mascara').fadeIn(300); 
	    $('#mascara').fadeTo("slow",0.5);
		    
		var scroll = $(document).scrollTop() + 150;
		    
		var left = ($(window).width() /2) - ( $(modal).width() / 2 );
		var top = ($(window).height() / 2) - ( $(modal).height() / 2 );
		     
		$(modal).css({'top':scroll,'left':left});
		$(modal).show();
			
		$("#loader-curtiram").show();
			
		$("body").css("overflow", "hidden");
			
		var content = $("#recebe-modal");
			
		window.setTimeout( function(){   
		$.ajax({
			url: action,
			type : "POST",
			data : $("#abrir-modal-desafio", li).serialize(),
			cache: false,
			success: function( response ){
				var data = $( '<div>'+response+'</div>' ).find('#wrap-modal-curtiram').html();
				$("#loader-curtiram").hide();	
				content.html( data ).hide();
				content.html( data ).show();
				   
			}
		  });
		}, 1000);
		return false;
	});
		   
	   $(document).on("click", "#mascara", function(){
		   $(this).hide();
	       $("#wrap-modal").hide();
	       $("#recebe-modal").empty();
	       $("body").css("overflow", "auto");
	   });
		   
	   $(document).on("click", ".close", function(){
		   $("#wrap-modal").hide();
		   $('#mascara').hide();
		   $("#recebe-modal").empty();
		   $("body").css("overflow", "auto");
	   });
		   
//FIM:  -------------- Modal usuarios curtiram Postagem Desafio ----------------
	
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

// 1.1: -------------- Ver mais comentarios ----------------
	$(document).on('submit', "#ver-mais-comentario", function() {
		
		$("#ver-mais-comentario").hide();
		$(".sk-circle").show();
		
		var content = $("#ul-comentarios");

		$.ajax({
			type : "POST",
			url : "mais_comentarios",
			data : $("#ver-mais-comentario").serialize(),
			success : function( response ) {
				//$("#containerFeed2").append(data);
				
				var data = $( '<div>'+response+'</div>' ).find('#ul-comentarios').html();
				// entra no conteudo da href procurando pela div #containerFeedGeral.
				
				content.append( data );
				
			},
			complete: function () {
		          $(".sk-circle").hide();
		          $("#ver-mais-comentario").remove();
			}
		});
		return false;
	});// 1.1: fim
	
// 1.2: -------------- Ver mais comentarios ----------------
	$(document).on('submit', "#ver-mais-curtidas", function() {
		
		$("#ver-mais-curtidas").hide();
		$(".load-mais-curtidas").show();
		
		var content = $(".ul-curtiram");
		
		window.setTimeout( function(){
		$.ajax({
			type : "POST",
			url : "mais_pingo",
			data : $("#ver-mais-curtidas").serialize(),
			success : function( response ) {
				//$("#containerFeed2").append(data);
				
				var data = $( '<div>'+response+'</div>' ).find('.ul-curtiram').html();
				// entra no conteudo da href procurando pela div #containerFeedGeral.
				
					content.append( data );
				
				
			},
			complete: function () {
		          $(".load-mais-curtidas").hide();
		          $("#ver-mais-curtidas").remove();
			}
		});
		}, 500 );
		return false;
	});// 1.2: fim
	
// 1.3: -------------- Ver mais postagens no perfil ----------------
	$(document).on('submit', "#ver-mais-perfil", function() {
		
		$("#ver-mais-perfil").hide();
		$(".sk-circle").show();
		
		var content = $("#wrap-postagens-perfil");

		$.ajax({
			type : "POST",
			url : "mais_posts_perfil",
			data : $("#ver-mais-perfil").serialize(),
			success : function( response ) {
				//$("#containerFeed2").append(data);
				
				var data = $( '<div>'+response+'</div>' ).find('#wrap-postagens-perfil').html();
				// entra no conteudo da href procurando pela div #containerFeedGeral.
				
				content.append( data );
				
			},
			complete: function () {
		          $(".sk-circle").hide();
		          $("#ver-mais-perfil").remove();
			}
		});
		return false;
	});// 1.3: fim

// 1.4: -------------- Ver mais postagens buscado ----------------
	$(document).on('submit', "#ver-mais-buscado", function() {
		
		$("#ver-mais-buscado").hide();
		$(".sk-circle").show();
		
		var content = $("#wrap-postagens-buscado");

		$.ajax({
			type : "POST",
			url : "mais_posts_buscado",
			data : $("#ver-mais-buscado").serialize(),
			success : function( response ) {
				//$("#containerFeed2").append(data);
				
				var data = $( '<div>'+response+'</div>' ).find('#wrap-postagens-buscado').html();
				// entra no conteudo da href procurando pela div #containerFeedGeral.
				
				content.append( data );
				
			},
			complete: function () {
		          $(".sk-circle").hide();
		          $("#ver-mais-buscado").remove();
			}
		});
		return false;
	});// 1.4: fim
	
// 1.5: -------------- Ver mais mensagens ----------------
	$(document).on('submit', "#ver-mais-msg", function() {
		
		$("#ver-mais-msg").hide();
		$(".sk-circle").show();
		
		var content = $("#ul-mensagens");
		
		//window.setTimeout( function(){
		$.ajax({
			type : "POST",
			url : "mais_mensagens",
			data : $("#ver-mais-msg").serialize(),
			
			success : function( response ) {
				//$("#containerFeed2").append(data);
				
				var data = $( '<div>'+response+'</div>' ).find('#ul-mensagens').html();
				// entra no conteudo da href procurando pela div #containerFeedGeral.
				
				content.append( data );
				
			},
			
			complete: function () {
		          $(".sk-circle").hide();
		          $("#ver-mais-msg").remove();
			}
		});
		//}, 500 );
		return false;
	});// 1.5: fim
// -------------- 2: faz o preview da imagem pra postar -----------
	function readURL(input) {

	    if (input.files && input.files[0]) {
	        var reader = new FileReader();

	        reader.onload = function (e) {
	            $('.img-preview').attr('src', e.target.result);
	        }

	        reader.readAsDataURL(input.files[0]);
	    }
	}// fim 2;
// -------------- 2.1: se o input file do post mudar -----------
	$(document).on("change", "#arquivo", function(){
		
		$("#btn-publicar").removeClass("disabled");
		$("#btn-publicar").removeAttr("disabled", "disabled");
		
		$("#preview").show();
		readURL(this);
		
	}); // 2.1: fim
	
	$(document).on("click", ".btn-preview", function(){
		$("#arquivo").val('');
		$("#preview").hide();
	});

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
				
				$("#preview").hide();
				
				$('.nav-times a').css("border-bottom","3px solid #337ab7");
				$("#li-geral").addClass("li-geral");

			}
		});
		
		e.preventDefault();
	});// 4: fim
});// fim document ready

// ------------ 5: quando clica em desafiar amigo direciona pra tela desafiar -------
$(document).on("click", "#btn-desafiar", function(){
	var ul = $(this).closest("#li-amigos");
	var id = $("#hide-desafio", ul).val();
	
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

//------------ 5.1: quando clica em desafiar amigo pela pesquisa direciona pra tela desafiar -------
$(document).on("click", ".btn-desafiar", function(){
	var ul = $(this).closest("#li-pesquisa");
	var id = $("#hide-desafio-pesquisa", ul).val();
	
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
});// 5.1: fim

//------------ 5.2: quando clica em desafiar amigo pela pesquisa amigos direciona pra tela desafiar -------
$(document).on("click", ".btn-desafiar-amigo", function(){
	var ul = $(this).closest("#li-pesquisa-amigos");
	var id = $("#hide-desafio-pesquisa", ul).val();
	
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
});// 5.2: fim

//------------ 5.3: envia solicitacao de amizade pelo resultado da pesquisa -------
$(document).on("click", ".btn-fazer-amizade", function(){
	var ul = $(this).closest("#li-pesquisa");
	var id = $("#hide-fazer-amizade", ul).val();
	
	$.ajax({
		url: 'fazer_amizade',
		data : {
			'cFazer_amizade' : id,
		},
		type: "post",
		cache : false,
		success: function(data){
			$("#btn-fazer-amizade", ul).attr("disabled", "disabled");
			$("#btn-fazer-amizade", ul).removeAttr("title");
			$("#btn-fazer-amizade", ul).removeClass("btn-primary btn-lg btn-fazer-amizade");
			$("#btn-fazer-amizade", ul).addClass("btn-solicitacao");
			$("#btn-fazer-amizade", ul).text("Solicitação Enviada");
		}
		
	});
	return false;
});// 5.3: fim

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
	var ul = $(this).closest("#li-pendentes");

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
	
			$(ul).fadeOut(200, function(){
				$(ul).remove();
	        });
			
			$(".notificacoes-desafios").load("timeline .ul-desafios");

		}
	});
	return false;
});// 7: fim

// --------------- 8: recusa desafio pendente -----------------
$(document).on("click", ".btn-recusar", function(){
	var ul = $(this).closest("#li-pendentes");

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

			$(ul).fadeOut(200, function(){
				$(ul).remove();
	        });
			
			$(".notificacoes-desafios").load("timeline .ul-desafios");
		
		}
	});
	return false;
});// 8: fim

//--------------- 9: remove msg -----------------
$(document).on("click", "#btn-remove-msg", function(){
	var container = $(this).closest(".li-mensagens");
	
	var hide_msg = $("#hide-msg", container).val();

	$.ajax({
		url: "apagar_mensagem",
		type: "post",
		data: {
			'cMensagem' : hide_msg,
		},
		success: function(data){

			$(container).fadeOut(200, function(){
         	   $(container).remove();
            });
			
			$(".notificacoes-msg").load("timeline .ul-msg");
		
		}
	});
	return false;
});// 9: fim

//--------------- 10: aceita solicitacao de amizade -----------------
$(document).on("click", "#btn-aceitar-solicitacao", function(){
	
	var ul = $(this).closest("#li-solicitacoes");
	//$("#ul-amigos").empty();
	var pedido_usuario_id = $("#pedido-usuario-id", ul).val();
	var pedido_solicitacao = $("#pedido-solicitacao", ul).val();
	var pedido_solicitacao_id = $("#pedido-solicitacao-id", ul).val();
	
	var content = $("#container-meus-amigos");
	var content_2 = $("#li-qtd-solicitacoes");
	
	$.ajax({
		url: "pedido_Solicitacao",
		type: "post",
		data: {
			'cPedido_usuario_id' : pedido_usuario_id,
			'cPedido_solicitacao' : pedido_solicitacao,
			'cPedido_solicitacao_id' : pedido_solicitacao_id,
		},
		success: function(response){
			
			//$("#container-meus-amigos").load("amigos #container-meus-amigos");
			
			$(ul).fadeOut(300, function(){
         	   $(ul).remove();
            });
			
			var data = $( '<div>'+response+'</div>' ).find('#container-meus-amigos').html();
			
			var data_2 = $( '<div>'+response+'</div>' ).find('#li-qtd-solicitacoes').html();
			
			// entra no conteudo da href procurando pela div #containerFeedGeral.
			 
			content.html( data ).hide();
				
			content_2.html( data_2 ).hide();
				
			content_2.html( data_2 ).show();
			    
			content.html( data ).show();
		}
	});
	return false;
});// 10: fim

//--------------- 11: recusa solicitacao de amizade -----------------
$(document).on("click", "#btn-recusar-solicitacao", function(){
	
	var ul = $(this).closest("#li-solicitacoes");

	var recusar_usuario_id = $("#recusar-usuario-id", ul).val();
	var recusar_solicitacao = $("#recusar-solicitacao", ul).val();
	var recusar_solicitacao_id = $("#recusar-solicitacao-id", ul).val();
	
	var content_2 = $("#li-qtd-solicitacoes");
	
	$.ajax({
		url: "pedido_Solicitacao",
		type: "post",
		data: {
			'cPedido_usuario_id' : recusar_usuario_id,
			'cPedido_solicitacao' : recusar_solicitacao,
			'cPedido_solicitacao_id' : recusar_solicitacao_id,
		},
		success: function(response){
			
			$(ul).fadeOut(300, function(){
	         	   $(ul).remove();
	        });
		
			var data_2 = $( '<div>'+response+'</div>' ).find('#li-qtd-solicitacoes').html();
			
			content_2.html( data_2 ).hide();
				
			content_2.html( data_2 ).show();
			
		}
	});
	return false;
});// 11: fim

//--------------- 12: direciona pra tela cumprir desafio -----------------
$(document).on("click", "#btn-cumprir-desafio", function(){
	
	var ul = $(this).closest("#li-cumprir");
	
	var content = $("#containerFeedGeral");
	var hide_desafio_cumprir = $("#hide-desafio-cumprir", ul).val();
	var url = "cumprir_desafio";
	
	content.html($(".loader").show());
	
	$.ajax({
		url: url,
		type: "post",
		data: {
			'id_desafio_ativo' : hide_desafio_cumprir,
		},
		success: function(response){
			
			var data = $( '<div>'+response+'</div>' ).find('#cumprir-desafio').html();
			// entra no conteudo da href procurando pela div #containerFeedGeral.
			 
			
			window.setTimeout( function(){ //atrasando para verificar o load.
				content.html( data ).hide();
			    
				content.html( data ).show('slide', {direction: 'up'}, 300, function(){
			    // a div que declarei vai receber o valor do sucesso do ajax.
			});
		    
		    //history.pushState('', 'New URL: '+url, url);  
			}, 500 );
			
		}
	});
	return false;
});// 12: fim

//--------------- 13: ajax para o lançar desafio -----------------
$(document).on('submit', '#form-postar-desafio', function(e) {
	
	var content = $("#containerFeed2");
	
	$.ajax({
		url : 'postar_desafio',
		type : 'POST',
		data : new FormData(this),
		processData : false,
		contentType : false,
		success : function( response ) {
			// show response from the php script.
			$("#text-post").val('');
			$("#arquivo").val('');
			$("#btn-publicar").addClass("disabled");
			$("#btn-publicar").attr("disabled", "disabled");
			
			var data = $( '<div>'+response+'</div>' ).find('#containerFeed2').html();
			// entra no conteudo da href procurando pela div #containerFeedGeral.
			 
			
			window.setTimeout( function(){ //atrasando para verificar o load.
				content.html( data ).hide();
			    
				content.html( data ).show('slide', {direction: 'up'}, 100, function(){
			    // a div que declarei vai receber o valor do sucesso do ajax.
			});
		    
		    //history.pushState('', 'New URL: '+url, url);  
			}, 100 );
		}
	});
	
	e.preventDefault();
});// 13: fim

// ------------------- 14: lançar desafio ------------------------
$(document).on("submit", "#form-lancar-desafio", function(){
	
	var content = $("#containerFeedGeral");
	
	$("#btn-lancar-desafio").val("Carregando..");
	
	var url = "timeline";
	
	$.ajax({
		url: "lancar_desafio",
		type: "post",
		data: $("#form-lancar-desafio").serialize(),
		success: function( response ){
			
			$("#li-ativos").load("timeline #wrap-badge-ativos");
			
			var data = $( '<div>'+response+'</div>' ).find('#containerFeedGeral').html();
			// entra no conteudo da href procurando pela div #containerFeedGeral.
			 
			
			window.setTimeout( function(){ //atrasando para verificar o load.
				content.html( data ).hide();
			    
				content.html( data ).show('slide', {direction: 'up'}, 300, function(){
			    // a div que declarei vai receber o valor do sucesso do ajax.
			});
		    
		    history.pushState('', 'New URL: '+url, url);  
			}, 1 );
			
			//$("#li-ativos").load("timeline #wrap-badge-ativos");
		}
	});
	return false;
});// 14: fim

//--------------- 15: verifica desafio cumprido -----------------
$(document).on("click", "#btn-verificar-desafio", function(){
	
	var ul = $(this).closest("#li-verificar");
	var content = $("#containerFeedGeral");
	
	var hide_verificar_desafio = $("#hide-verificar-desafio", ul).val();
	
	var url = "verificar_desafio";
	
	content.html($(".loader").show());
	
	$.ajax({
		url: url,
		type: "post",
		data: {
			'id_desafio_ativo' : hide_verificar_desafio,
		},
		success: function(response){
			var data = $( '<div>'+response+'</div>' ).find('#verificar-desafio').html();
			// entra no conteudo da href procurando pela div #containerFeedGeral.
			 
			
			window.setTimeout( function(){ //atrasando para verificar o load.
				content.html( data ).hide();
			    
				content.html( data ).show('slide', {direction: 'up'}, 300, function(){
			    // a div que declarei vai receber o valor do sucesso do ajax.
			});
		    
		    //history.pushState('', 'New URL: '+url, url);  
			}, 500 );
			
		}
	});
	return false;
});// 15: fim

//------------------- 15: atribui pontos a um desafio ------------------------
$(document).on("submit", "#form-atribuir-desafio", function(){
	
	var content = $("#containerFeedGeral");
	
	var usuario = $("#usuario-cumprido").val();
	
	$("#btn-atribuir-desafio").val("Atribuindo..");
	
	$.ajax({
		url: "atribuir_desafio",
		type: "post",
		data: $("#form-atribuir-desafio").serialize(),
		success: function( response ){
			
			alert("Pontos atribuidos para:" + " " + usuario);
			
			$("#li-cumpridos").load("timeline #wrap-badge-cumpridos");
			
			var data = $( '<div>'+response+'</div>' ).find('#desafios-cumpridos').html();
			// entra no conteudo da href procurando pela div #containerFeedGeral.
			 
			
			window.setTimeout( function(){ //atrasando para verificar o load.
				content.html( data ).hide();
			    
				content.html( data ).show('slide', {direction: 'up'}, 300, function(){
			    // a div que declarei vai receber o valor do sucesso do ajax.
			});
		    
		    //history.pushState('', 'New URL: '+url, url);  
			}, 500 );
		}
	});
	return false;
});// 15: fim ---------------- atribui pontos a um desafio -------------------

//------------------- 16: recusa pontos a um desafio ------------------------
$(document).on("submit", "#form-recusar-desafio", function(){
	
	var content = $("#containerFeedGeral");
	
	var usuario = $("#usuario-cumprido").val();
	
	$("#btn-recusar-desafio").val("Recusando..");
	
	$.ajax({
		url: "atribuir_desafio",
		type: "post",
		data: $("#form-recusar-desafio").serialize(),
		success: function( response ){
			
			alert("Pontos recusados para:" + " " + usuario);
			
			
			$("#li-cumpridos").load("timeline #wrap-badge-cumpridos");
			
			
			var data = $( '<div>'+response+'</div>' ).find('#desafios-cumpridos').html();
			// entra no conteudo da href procurando pela div #containerFeedGeral.
			 
			
			window.setTimeout( function(){ //atrasando para verificar o load.
				content.html( data ).hide();
			    
				content.html( data ).show('slide', {direction: 'up'}, 300, function(){
			    // a div que declarei vai receber o valor do sucesso do ajax.
			});
		    
		    //history.pushState('', 'New URL: '+url, url);  
			}, 500 );
		}
	});
	return false;
});// 16: fim ---------------- recusa pontos a um desafio -------------------

//--------------- 17: lança um desafio ao amigo pelo menu desafiar -------------//
$(document).on("submit", "#form-desafiar-amigos", function(){
	
	$.ajax({
		url: 'lancar_desafios',
		data : $("#form-desafiar-amigos").serialize(),
		type: "post",
		cache : false,
		success: function(data){
			
			alert(data);
		}
		
	});
	return false;
});// 17: fim

//--------------- 18: posta comentario2 em uma publicacao -----------------
$(document).on("submit", "#postar-comentario-2", function(){
	
	var content = $("#containerFeed2");		
	var textarea = $(".input-comentario").val();
	
	$.ajax({
		url: "postarComentarios2",
		type: "post",
		data: $("#postar-comentario-2").serialize(),
		success: function( response ){
			
			var textarea = $(".input-comentario").val('');
			
			var data = $( '<div>'+response+'</div>' ).find('#containerFeed2').html();
			// entra no conteudo da href procurando pela div #containerFeedGeral.
			 
			
			window.setTimeout( function(){ //atrasando para verificar o load.
				content.html( data ).hide();
			    
				content.html( data ).show('slide', {direction: 'up'}, 300, function(){
			    // a div que declarei vai receber o valor do sucesso do ajax.
			});
		    
		    //history.pushState('', 'New URL: '+url, url);  
			}, 500 );
		}
	});
	return false;
});// 18: fim -------- posta comentario2 em uma publicacao -----------------

//----------------- 19: direciona para tela editar perfil ------------------
$(document).on("submit", "#editar-perfil", function(){
	
	var content = $("#containerFeedGeral");	
	var url = "editarPerfil";
	
	//content.html($(".loader").show());
	
	$.ajax({
		url: "editarPerfil",
		type: "post",
		data: $("#editar-perfil").serialize(),
		success: function(response){
			var data = $( '<div>'+response+'</div>' ).find('#container-editar-perfil').html();
			// entra no conteudo da href procurando pela div #containerFeedGeral.
			 
			
			window.setTimeout( function(){ //atrasando para verificar o load.
				content.html( data ).hide();
			    
				content.html( data ).show('slide', {direction: 'up'}, 300, function(){
			    // a div que declarei vai receber o valor do sucesso do ajax.
			});
		    
		    history.pushState('', 'New URL: ', url);  
			}, 0 );
		}
	});
	return false;
});// fim: ----------------- 20: atualiza informações do perfil ------------------

$(document).on("submit", "#atualizar-informacoes", function(){
	
	var content = $("#containerFeedGeral");	
	var content_2 = $("#containerPerfil");
	var url = "perfil";
	
	//content.html($(".loader").show());
	
	$.ajax({
		url: "atualizarInformacoes",
		type: "post",
		data : new FormData(this),
		processData : false,
		contentType : false,
		success: function(response){
			var data = $( '<div>'+response+'</div>' ).find('#containerFeedGeral').html();
			
			var data_2 = $( '<div>'+response+'</div>' ).find('#containerPerfil').html();
			
			// entra no conteudo da href procurando pela div #containerFeedGeral.
			 
			
			window.setTimeout( function(){ //atrasando para verificar o load.
				
				content.html( data ).hide();
				
				content_2.html( data_2 ).hide();
				
				content_2.html( data_2 ).show();
			    
				content.html( data ).show('slide', {direction: 'up'}, 300, function(){
			    // a div que declarei vai receber o valor do sucesso do ajax.
			});
		    
		    history.pushState('', 'New URL: ', url);  
			}, 0 );
		}
	});
	return false;
});// fim: ----------------- 20: atualiza informações do perfil ------------------

// 21 ----------------- pesquisa geral -------------------------------------------

$(document).on("submit", "#form-pesquisa", function(){
	
	var content = $("#wrap-container-amigos");
	content.html($(".loader").show());
	
	$.ajax({
		url: "pesquisa",
		type: "post",
		data: $("#form-pesquisa").serialize(),
		success: function(response){
			var data = $( '<div>'+response+'</div>' ).find('#wrap-resultado-pesquisa').html();
			// entra no conteudo da href procurando pela div #containerFeedGeral.
			 
			
			window.setTimeout( function(){ //atrasando para verificar o load.
				content.html( data ).hide();
			    
				content.html( data ).show('slide', {direction: 'up'}, 300, function(){
			    // a div que declarei vai receber o valor do sucesso do ajax.
			});
		    
		    //history.pushState('', 'New URL: ', url);  
			}, 0 );
		}
	});
	return false;
});// 21 fim ----------------- pesquisa geral -----------------------------------