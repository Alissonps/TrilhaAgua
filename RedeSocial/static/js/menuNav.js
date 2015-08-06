$(document).ready(function(){
	$(document).on("click", "#menu-ul a", function(){

		var content = $("#containerFeedGeral");// div que recebe os dados.
		var href = $(this).attr("href");// obtendo href do menu clicado.

		$('#menu-ul a').css("border-left","4px solid #337ab7").css("background-color", "#f7f7f7");
	    $(this).css("border-left","4px solid #F8C51B").css( "background-color", "#F0F0F0");
		
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
			    
			    history.pushState('', 'New URL: '+href, href);  
				}, 500 );
			}
		});
		return false;
	});

/*-------- 2: Quando a página é voltada essa função pinta todas a href na sua cor original e
 * carrega na div ContainerFeedGeral o conteudo da href voltada com enfase na div ContainerFeedGeral do href ------ */
	
	window.onpopstate = function(event) {
		var content = $("#containerFeedGeral");
		content.html($(".loader").show());
		$('#menu-ul a').css("border-left","4px solid #337ab7").css("background-color", "#f7f7f7");
		
	    
        console.log("pathname: "+location.pathname);
        $("#containerFeedGeral").load(location.href+" #containerFeedGeral>*","");

/*-------- 3: Quando a página é voltada essa função pinta a href conrrespondente a página voltada ------ */          
        var link = (location.href);
		
        $(function() {
        	$("#menu-ul a").each(function() {
        		if (this.href == link) {
        			$(this).css("border-left","4px solid #F8C51B").css( "background-color", "#F0F0F0");
        		};
        	});
        });/* Fim 3*/
      };/* Fim 2*/
      
/*-------- 4: Quando atualiza a página essa função pinta a href conrrespondente a atual url ------ */
      
      $(function() {
      	$("#menu-ul a").each(function() {
      		var path = window.location.pathname; // Returns path only
      		var url      = window.location.href; 
      		
      		if (this.href == url) {
      			$(this).css("border-left","4px solid #F8C51B").css( "background-color", "#F0F0F0");
      		};
      	});
      }); /* Fim 4*/
/*-------- 5: Navegação notificacao-ul ------ */      
  	$(document).on("click", "#notificacao-ul a", function(){

		var content = $("#containerFeedGeral");// div que recebe os dados.
		var href = $(this).attr("href");// obtendo href do menu clicado.

		//$('#menu-ul a').css("border-left","4px solid #337ab7").css("background-color", "#f7f7f7");
	    //$(this).css("border-left","4px solid #F8C51B").css( "background-color", "#F0F0F0");
		
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
			    
			    history.pushState('', 'New URL: '+href, href);  
				}, 500 );
			}
		});
		return false;
	});/* Fim 5*/
});