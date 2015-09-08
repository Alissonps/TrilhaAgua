$(document).ready(function(){
	// Função que carrega com ajax a href correspondente;
	$(document).on("click", "#menu-ul a", function(){

		var content = $("#containerFeedGeral");// div que recebe os dados.
		var href = $(this).attr("href");// obtendo href do menu clicado.
		var titulo = $(this).attr("title");
		$('#menu-ul a').css("border-left","4px solid #337ab7").css("background-color", "#f7f7f7");
	    $(this).css("border-left","4px solid #F8C51B").css( "background-color", "#F0F0F0");
	    
	    content.html($(".loader").show());
	    
	    //window.history.pushState("", "", "/");
	    
	    $.ajax({
			url: href,
			success: function( response ){
				var data = $( '<div>'+response+'</div>' ).find('#containerFeedGeral').html();
				// entra no conteudo da href procurando pela div #containerFeedGeral.
				 
				
					content.html( data ).hide();
				    
					content.html( data ).show('slide', {direction: 'up'}, 300, function(){
				    // a div que declarei vai receber o valor do sucesso do ajax.
					
					$("table #ranking:odd", content).css("background", "rgb(235,235,235)");
				});
				
				document.title = titulo;
				window.history.pushState('', titulo, href);  
				
			}
		});
		return false;
	});//FIM Função que carrega com ajax a href correspondente;
/*-------- 2: Quando a página é voltada essa função pinta todas a href na sua cor original e
 * carrega na div ContainerFeedGeral o conteudo da href voltada com enfase na div ContainerFeedGeral do href ------ */
	
	window.onpopstate = function(event) {
		
		var link = (location.href);
		var content = $("#containerFeedGeral");
		
		content.html($(".loader").show());
		
		$('#menu-ul a').css("border-left","4px solid #337ab7").css("background-color", "#f7f7f7");
		
		console.log("pathname: "+location.pathname);
        
		//Função q carrega oq tem dentro da div ContainerFeedGeral quando Voltada;
		$("#containerFeedGeral").load(location.href+" #containerFeedGeral>*","", function(){
        	$("#li-geral", content).removeClass("li-geral");
        	
        	// Verifica em qual timeline está e pinta ela da cor correspondente;
        	$(function() {	
            	$(".nav-times a").each(function() {
            		
            		if (this.href == link) {
            			$(this).css("border-bottom","3px solid #ff8901");
            			
            			$("#menu-ul a[href=timeline").css("border-left","4px solid #F8C51B").css( "background-color", "#F0F0F0");
            		};
            	});
            });// FIM Verifica em qual timeline está e pinta ela da cor correspondente;
        	
        	// Verifica em qual ranking está e pinta ela da cor correspondente;
        	$(function() {	
            	$(".nav-ranks a").each(function() {
            		if (this.href == link) {
            			$(this).css("border-bottom","3px solid #ff8901");
            			$("table #ranking:odd").css("background", "rgb(235,235,235)");
            			
            			$("#menu-ul a[href=rankings").css("border-left","4px solid #F8C51B").css( "background-color", "#F0F0F0");
            		};
            	});
            });// FIM Verifica em qual ranking está e pinta ela da cor correspondente;
        });// FIM //Função q carrega oq tem dentro da div ContainerFeedGeral quando Voltada;

/*-------- 3: Quando a página é voltada essa função pinta a href conrrespondente a página voltada ------ */          
		
        $(function() {
        	$("#menu-ul a").each(function() {
        		if (this.href == link) {
        			var titulo = $(this).attr("title");
            		$("title").text(titulo);
        			$(this).css("border-left","4px solid #F8C51B").css( "background-color", "#F0F0F0");
        		};
        	});
        });/* Fim 3*/
        
        // 4: funcao que altera title da pagina de acordo com o menu notificacao-ul
        $(function() {
        	$("#notificacao-ul a").each(function() {
        		if (this.href == link) {
        			var titulo = $(this).attr("title");
            		$("title").text(titulo);
        		};
        	});
        });// 4: FIM funcao que altera title da pagina de acordo com o menu notificacao-ul
        
      };/* Fim 2* popstate/
      
/*-------- 4: Quando atualiza a página essa função pinta a href conrrespondente a atual url ------ */
      
      $(function() {
      	$("#menu-ul a").each(function() {
      		var path = window.location.pathname; // Returns path only
      		var url      = window.location.href; 
      		
      		if (this.href == url) {
      			var titulo = $(this).attr("title");
        		$("title").text(titulo);
      			$(this).css("border-left","4px solid #F8C51B").css( "background-color", "#F0F0F0");
      		};
      	});
      }); /* Fim 4*/
      
/*-------- 5: Navegação notificacao-ul ------ */      
  	$(document).on("click", "#notificacao-ul a", function(){

		var content = $("#containerFeedGeral");// div que recebe os dados.
		var href = $(this).attr("href");// obtendo href do menu clicado.
		var titulo = $(this).attr("title");
		var amigos = "amigos";
		
		$('#menu-ul a').css("border-left","4px solid #337ab7").css("background-color", "#f7f7f7");
	    //$(this).css("border-left","4px solid #F8C51B").css( "background-color", "#F0F0F0");
		
		//1: verifica se a href clicada é igual a "amigos", se for pinta o menu-ul a[amigos] com a borda laranja
		if(href == amigos){
			$("#menu-ul a[href*=amigos]").css("border-left","4px solid #F8C51B").css( "background-color", "#F0F0F0");
		}//1: FIM verifica se a href clicada é igual a "amigos", se for pinta o menu-ul a[amigos] com a borda laranja
		
	    content.html($(".loader").show());
		
	    $.ajax({
			url: href,
			success: function( response ){
				var data = $( '<div>'+response+'</div>' ).find('#containerFeedGeral').html();
				// entra no conteudo da href procurando pela div #containerFeedGeral.
				 
				
				window.setTimeout( function(){ //atrasando para verificar o load.
					content.html( data ).hide();
				    
					content.html( data ).show('slide', {direction: 'up'}, 300, function(){
				    // a div que declarei vai receber o valor do sucesso do ajax.
				});
				
				document.title = titulo;
				window.history.pushState('', titulo, href);   
				}, 500 );
			}
		});
		return false;
	});/* Fim 5*/
  	
/*-------- 6: Navegação usuarios curtiram ------ */      
  	$(document).on("submit", "#form-u-curtiu", function(){
  		var feed = $(this).closest(".containerPostagem");
  		
  		var hide_u_curtiu = $("#hide-u-curtiu", feed).val();
		var content = $("#containerFeedGeral");// div que recebe os dados.

		//$('#menu-ul a').css("border-left","4px solid #337ab7").css("background-color", "#f7f7f7");
	    //$(this).css("border-left","4px solid #F8C51B").css( "background-color", "#F0F0F0");
		
	    content.html($(".loader").show());
		
	    $.ajax({
			url: "usuarios_curtiram",
			type: "post",
			data: {
				"cID_post" : hide_u_curtiu,
			},
			success: function( response ){
				var data = $( '<div>'+response+'</div>' ).find('#containerFeedGeral').html();
				// entra no conteudo da href procurando pela div #containerFeedGeral.
				 
				
				window.setTimeout( function(){ //atrasando para verificar o load.
					content.html( data ).hide();
				    
					content.html( data ).show('slide', {direction: 'up'}, 300, function(){
				    // a div que declarei vai receber o valor do sucesso do ajax.
				});
			    
			    //history.pushState('', 'New URL: '+href, href);  
				}, 500 );
			}
		});
		return false;
	});/* Fim 6--------  Navegação usuarios curtiram ------ */
  	
/*-------- 6.1: Navegação usuarios buscados ------ */      
  	$(document).on("submit", "#form-busca-usuario", function(){
  		var feed = $(this).closest(".containerPostagem");
  		
  		var hide_u_curtiu = $("#hide-u-curtiu", feed).val();
		var content = $("#containerFeedGeral");// div que recebe os dados.
		var action = $("#form-busca-usuario", feed).attr("action");
		//$('#menu-ul a').css("border-left","4px solid #337ab7").css("background-color", "#f7f7f7");
	    //$(this).css("border-left","4px solid #F8C51B").css( "background-color", "#F0F0F0");
		
	    content.html($(".loader").show());
		
	    $.ajax({
			url: action,
			type: "post",
			data: $("#form-busca-usuario").serialize(),
			success: function( response ){
				var data = $( '<div>'+response+'</div>' ).find('#containerFeedGeral').html();
				// entra no conteudo da href procurando pela div #containerFeedGeral.
				 
				$('#menu-ul a').css("border-left","4px solid #337ab7").css("background-color", "#f7f7f7")
				
				window.setTimeout( function(){ //atrasando para verificar o load.
					content.html( data ).hide();
				    
					content.html( data ).show('slide', {direction: 'up'}, 300, function(){
				    // a div que declarei vai receber o valor do sucesso do ajax.
				});
			    
			    history.pushState('', 'New URL: ', action);  
				}, 500 );
			}
		});
		return false;
	});/* Fim 6.1--------  Navegação usuarios buscados ------ */ 
  	
/*-------- 6.2: Navegação usuarios buscados desafios ------ */      
  	$(document).on("submit", "#form-busca-usuario-desafio", function(){
  		var feed = $(this).closest(".containerPostagemDesafio");
  		
  		var hide_u_curtiu = $("#hide-u-curtiu", feed).val();
		var content = $("#containerFeedGeral");// div que recebe os dados.
		var action = $("#form-busca-usuario-desafio", feed).attr("action");
		//$('#menu-ul a').css("border-left","4px solid #337ab7").css("background-color", "#f7f7f7");
	    //$(this).css("border-left","4px solid #F8C51B").css( "background-color", "#F0F0F0");
		
	    content.html($(".loader").show());
		
	    $.ajax({
			url: action,
			type: "post",
			data: $("#form-busca-usuario-desafio").serialize(),
			success: function( response ){
				var data = $( '<div>'+response+'</div>' ).find('#containerFeedGeral').html();
				// entra no conteudo da href procurando pela div #containerFeedGeral.
				 
				$('#menu-ul a').css("border-left","4px solid #337ab7").css("background-color", "#f7f7f7");
				
				window.setTimeout( function(){ //atrasando para verificar o load.
					content.html( data ).hide();
				    
					content.html( data ).show('slide', {direction: 'up'}, 300, function(){
				    // a div que declarei vai receber o valor do sucesso do ajax.
				});
			    
			    history.pushState('', 'New URL: ', action);  
				}, 500 );
			}
		});
		return false;
	});/* Fim 6.2--------  Navegação usuarios buscados desafios ------ */ 
  	
/*-------- 6.3: Navegação usuarios buscados rankings ------ */      
  	$(document).on("submit", "#form-busca-usuario-rank", function(){
  		var tr = $(this).closest("#ranking");
  		
		var content = $("#containerFeedGeral");// div que recebe os dados.
		var action = $("#form-busca-usuario-rank", tr).attr("action");
		
	    //$(this).css("border-left","4px solid #F8C51B").css( "background-color", "#F0F0F0");
		
	    content.html($(".loader").show());
		
	    $.ajax({
			url: action,
			type: "post",
			data: $("#form-busca-usuario-rank").serialize(),
			success: function( response ){
				var data = $( '<div>'+response+'</div>' ).find('#containerFeedGeral').html();
				// entra no conteudo da href procurando pela div #containerFeedGeral.
				 
				$('#menu-ul a').css("border-left","4px solid #337ab7").css("background-color", "#f7f7f7");
				
				window.setTimeout( function(){ //atrasando para verificar o load.
					content.html( data ).hide();
				    
					content.html( data ).show('slide', {direction: 'up'}, 300, function(){
				    // a div que declarei vai receber o valor do sucesso do ajax.
				});
			    
			    history.pushState('', 'New URL: ', action);  
				}, 0 );
			}
		});
		return false;
	});/* Fim 6.3--------  Navegação usuarios buscados rankings ------ */ 
  	
/*-------- 6.4: Navegação usuarios buscados pesquisa geral ------ */      
  	$(document).on("submit", "#form-busca-pesquisa-geral", function(){
  		var li = $(this).closest("#li-pesquisa");
  		
		var content = $("#containerFeedGeral");// div que recebe os dados.
		var action = $("#form-busca-pesquisa-geral", li).attr("action");
		
	    //$(this).css("border-left","4px solid #F8C51B").css( "background-color", "#F0F0F0");
		
	    content.html($(".loader").show());
		
	    $.ajax({
			url: action,
			type: "post",
			data: $("#form-busca-pesquisa-geral").serialize(),
			success: function( response ){
				var data = $( '<div>'+response+'</div>' ).find('#containerFeedGeral').html();
				// entra no conteudo da href procurando pela div #containerFeedGeral.
				 
				$('#menu-ul a').css("border-left","4px solid #337ab7").css("background-color", "#f7f7f7");
				
				window.setTimeout( function(){ //atrasando para verificar o load.
					content.html( data ).hide();
				    
					content.html( data ).show('slide', {direction: 'up'}, 300, function(){
				    // a div que declarei vai receber o valor do sucesso do ajax.
				});
			    
			    history.pushState('', 'New URL: ', action);  
				}, 0 );
			}
		});
		return false;
	});/* Fim 6.4-------- : Navegação usuarios buscados pesquisa geral ------ */

/*-------- 6.5: Navegação usuarios buscados amigos ------ */      
  	$(document).on("submit", "#form-busca-usuario-amigos", function(){
  		var li = $(this).closest("#li-amigos");
  		
		var content = $("#containerFeedGeral");// div que recebe os dados.
		var action = $("#form-busca-usuario-amigos", li).attr("action");
		
	    //$(this).css("border-left","4px solid #F8C51B").css( "background-color", "#F0F0F0");
		
	    content.html($(".loader").show());
		
	    $.ajax({
			url: action,
			type: "post",
			data: $("#form-busca-usuario-amigos").serialize(),
			success: function( response ){
				var data = $( '<div>'+response+'</div>' ).find('#containerFeedGeral').html();
				// entra no conteudo da href procurando pela div #containerFeedGeral.
				 
				$('#menu-ul a').css("border-left","4px solid #337ab7").css("background-color", "#f7f7f7");
				
				window.setTimeout( function(){ //atrasando para verificar o load.
					content.html( data ).hide();
				    
					content.html( data ).show('slide', {direction: 'up'}, 300, function(){
				    // a div que declarei vai receber o valor do sucesso do ajax.
				});
			    
			    history.pushState('', 'New URL: ', action);  
				}, 0 );
			}
		});
		return false;
	});/* Fim 6.5-------- : Navegação usuarios buscados amigos ------ */
  	
/*-------- 6.6: Navegação usuarios buscados solicitacao amigos ------ */      
  	$(document).on("submit", "#form-busca-usuario-solicitacoes", function(){
  		var li = $(this).closest("#li-solicitacoes");
  		
		var content = $("#containerFeedGeral");// div que recebe os dados.
		var action = $("#form-busca-usuario-solicitacoes", li).attr("action");
		
	    //$(this).css("border-left","4px solid #F8C51B").css( "background-color", "#F0F0F0");
		
	    content.html($(".loader").show());
		
	    $.ajax({
			url: action,
			type: "post",
			data: $("#form-busca-usuario-solicitacoes").serialize(),
			success: function( response ){
				var data = $( '<div>'+response+'</div>' ).find('#containerFeedGeral').html();
				// entra no conteudo da href procurando pela div #containerFeedGeral.
				 
				$('#menu-ul a').css("border-left","4px solid #337ab7").css("background-color", "#f7f7f7");
				
				window.setTimeout( function(){ //atrasando para verificar o load.
					content.html( data ).hide();
				    
					content.html( data ).show('slide', {direction: 'up'}, 300, function(){
				    // a div que declarei vai receber o valor do sucesso do ajax.
				});
			    
			    history.pushState('', 'New URL: ', action);  
				}, 0 );
			}
		});
		return false;
	});/* Fim 6.6-------- : Navegação usuarios buscados solicitacao amigos ------ */ 
  	
/*-------- 6.7: Navegação usuarios buscados pesquisa amigos ------ */      
  	$(document).on("submit", "#form-busca-usuario-pesquisa-amigos", function(){
  		var li = $(this).closest("#li-pesquisa-amigos");
  		
		var content = $("#containerFeedGeral");// div que recebe os dados.
		var action = $("#form-busca-usuario-pesquisa-amigos", li).attr("action");
		
	    //$(this).css("border-left","4px solid #F8C51B").css( "background-color", "#F0F0F0");
		
	    content.html($(".loader").show());
		
	    $.ajax({
			url: action,
			type: "post",
			data: $("#form-busca-usuario-pesquisa-amigos").serialize(),
			success: function( response ){
				var data = $( '<div>'+response+'</div>' ).find('#containerFeedGeral').html();
				// entra no conteudo da href procurando pela div #containerFeedGeral.
				 
				$('#menu-ul a').css("border-left","4px solid #337ab7").css("background-color", "#f7f7f7");
				
				window.setTimeout( function(){ //atrasando para verificar o load.
					content.html( data ).hide();
				    
					content.html( data ).show('slide', {direction: 'up'}, 300, function(){
				    // a div que declarei vai receber o valor do sucesso do ajax.
				});
			    
			    history.pushState('', 'New URL: ', action);  
				}, 0 );
			}
		});
		return false;
	});/* Fim 6.6-------- : Navegação usuarios buscados pesquisa amigos ------ */
  	
/*-------- 6.7: Navegação usuarios buscados pendentes ------ */      
  	$(document).on("submit", "#form-busca-usuario-pendentes", function(){
  		var li = $(this).closest("#li-pendentes");
  		
		var content = $("#containerFeedGeral");// div que recebe os dados.
		var action = $("#form-busca-usuario-pendentes", li).attr("action");
		
	    //$(this).css("border-left","4px solid #F8C51B").css( "background-color", "#F0F0F0");
		
	    content.html($(".loader").show());
		
	    $.ajax({
			url: action,
			type: "post",
			data: $("#form-busca-usuario-pendentes").serialize(),
			success: function( response ){
				var data = $( '<div>'+response+'</div>' ).find('#containerFeedGeral').html();
				// entra no conteudo da href procurando pela div #containerFeedGeral.
				 
				$('#menu-ul a').css("border-left","4px solid #337ab7").css("background-color", "#f7f7f7");
				
				window.setTimeout( function(){ //atrasando para verificar o load.
					content.html( data ).hide();
				    
					content.html( data ).show('slide', {direction: 'up'}, 300, function(){
				    // a div que declarei vai receber o valor do sucesso do ajax.
				});
			    
			    history.pushState('', 'New URL: ', action);  
				}, 0 );
			}
		});
		return false;
	});/* Fim 6.7-------- : Navegação usuarios buscados pendentes ------ */ 
  	
  	/*-------- 6.8: Navegação usuarios buscados ativos ------ */      
  	$(document).on("submit", "#form-busca-usuario-ativos", function(){
  		var li = $(this).closest("#li-cumprir");
  		
		var content = $("#containerFeedGeral");// div que recebe os dados.
		var action = $("#form-busca-usuario-ativos", li).attr("action");
		
	    //$(this).css("border-left","4px solid #F8C51B").css( "background-color", "#F0F0F0");
		
	    content.html($(".loader").show());
		
	    $.ajax({
			url: action,
			type: "post",
			data: $("#form-busca-usuario-ativos").serialize(),
			success: function( response ){
				var data = $( '<div>'+response+'</div>' ).find('#containerFeedGeral').html();
				// entra no conteudo da href procurando pela div #containerFeedGeral.
				 
				$('#menu-ul a').css("border-left","4px solid #337ab7").css("background-color", "#f7f7f7");
				
				window.setTimeout( function(){ //atrasando para verificar o load.
					content.html( data ).hide();
				    
					content.html( data ).show('slide', {direction: 'up'}, 300, function(){
				    // a div que declarei vai receber o valor do sucesso do ajax.
				});
			    
			    history.pushState('', 'New URL: ', action);  
				}, 0 );
			}
		});
		return false;
	});/* Fim 6.8-------- : Navegação usuarios buscados ativos ------ */ 
  	
/*-------- 7: Navegação comentarios da publicacao ------ */      
  	$(document).on("submit", "#form-comentarios", function(){
  		var feed = $(this).closest(".containerPostagem");
  		
  		var hide_comentarios = $("#hide-comentarios", feed).val();
		var content = $("#containerFeedGeral");// div que recebe os dados.

		//$('#menu-ul a').css("border-left","4px solid #337ab7").css("background-color", "#f7f7f7");
	    //$(this).css("border-left","4px solid #F8C51B").css( "background-color", "#F0F0F0");
		
	    content.html($(".loader").show());
		
	    $.ajax({
			url: "visualizarComentarios",
			type: "post",
			data: {
				"cPost" : hide_comentarios,
			},
			success: function( response ){
				var data = $( '<div>'+response+'</div>' ).find('#containerFeedGeral').html();
				// entra no conteudo da href procurando pela div #containerFeedGeral.
				 
				
				window.setTimeout( function(){ //atrasando para verificar o load.
					content.html( data ).hide();
				    
					content.html( data ).show('slide', {direction: 'up'}, 300, function(){
				    // a div que declarei vai receber o valor do sucesso do ajax.
				});
			    
			    //history.pushState('', 'New URL: '+href, href);  
				}, 500 );
			}
		});
		return false;
	});/* Fim 7: Navegação comentarios da publicacao ------ */ 
  	
/*-------- 8: Navegação usuarios curtiram desafios ------ */      
  	$(document).on("submit", "#form-u-curtiu-desafio", function(){
  		var feed = $(this).closest(".containerPostagemDesafio");
  		
  		var hide_u_curtiu = $("#hide-u-curtiu", feed).val();
		var content = $("#containerFeedGeral");// div que recebe os dados.

		//$('#menu-ul a').css("border-left","4px solid #337ab7").css("background-color", "#f7f7f7");
	    //$(this).css("border-left","4px solid #F8C51B").css( "background-color", "#F0F0F0");
		
	    content.html($(".loader").show());
		
	    $.ajax({
			url: "usuarios_curtiram",
			type: "post",
			data: {
				"cID_post" : hide_u_curtiu,
			},
			success: function( response ){
				var data = $( '<div>'+response+'</div>' ).find('#containerFeedGeral').html();
				// entra no conteudo da href procurando pela div #containerFeedGeral.
				 
				
				window.setTimeout( function(){ //atrasando para verificar o load.
					content.html( data ).hide();
				    
					content.html( data ).show('slide', {direction: 'up'}, 300, function(){
				    // a div que declarei vai receber o valor do sucesso do ajax.
				});
			    
			    //history.pushState('', 'New URL: '+href, href);  
				}, 500 );
			}
		});
		return false;
	});/* Fim 8:--------  Navegação usuarios curtiram desafios ------ */ 
  	
/*-------- 9: Navegação comentarios da publicacao desafios ------ */      
  	$(document).on("submit", "#form-comentarios-desafio", function(){
  		var feed = $(this).closest(".containerPostagemDesafio");
  		
  		var hide_comentarios = $("#hide-comentarios", feed).val();
		var content = $("#containerFeedGeral");// div que recebe os dados.

		//$('#menu-ul a').css("border-left","4px solid #337ab7").css("background-color", "#f7f7f7");
	    //$(this).css("border-left","4px solid #F8C51B").css( "background-color", "#F0F0F0");
		
	    content.html($(".loader").show());
		
	    $.ajax({
			url: "visualizarComentarios",
			type: "post",
			data: {
				"cPost" : hide_comentarios,
			},
			success: function( response ){
				var data = $( '<div>'+response+'</div>' ).find('#containerFeedGeral').html();
				// entra no conteudo da href procurando pela div #containerFeedGeral.
				 
				
				window.setTimeout( function(){ //atrasando para verificar o load.
					content.html( data ).hide();
				    
					content.html( data ).show('slide', {direction: 'up'}, 300, function(){
				    // a div que declarei vai receber o valor do sucesso do ajax.
				});
			    
			    //history.pushState('', 'New URL: '+href, href);  
				}, 500 );
			}
		});
		return false;
	});/* Fim 9: Navegação comentarios da publicacao desafios ------ */  
});// fim document ready