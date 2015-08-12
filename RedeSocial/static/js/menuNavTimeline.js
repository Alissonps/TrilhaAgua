	$(document).on("click", ".nav-times a", function(){

		var content = $("#containerFeed2");// div que recebe os dados.
		var href = $(this).attr("href");// obtendo href do menu clicado.
		
		$("#li-geral").removeClass("li-geral");
		$('.nav-times a').css("border-bottom","3px solid #337ab7");
		
	    $(this).css("border-bottom","3px solid #ff8901");
	    $("#menu-ul a[href=timeline]").css("border-left","4px solid #F8C51B").css( "background-color", "#F0F0F0");
		
	    content.html($(".loader").show());
	    
	    //window.history.pushState("", "", "/");
	    
	    $.ajax({
			url: href,
			beforeSend: function () {
				//$(this).text("carregando..");
				content.html($(".loader").show());
		    },
			success: function( response ){
				var data = $( '<div>'+response+'</div>' ).find('#containerFeed2').html();
				// entra no conteudo da href procurando pela div #containerFeedGeral.
				 
				
				
				window.setTimeout( function(){ //atrasando para verificar o load.
					content.html( data ).hide();
				    
					content.html( data ).show('slide', {direction: 'up'}, 300, function(){
				    // a div que declarei vai receber o valor do sucesso do ajax.
				});
			    
				window.history.pushState('', 'New URL: ', href);  
				}, 500 );
			},
	    
		    complete: function () {
		          content.html($("#containerFeed2").hide());
			}
		});
		return false;
	});