	$(document).ready(function(){
		var content = $('#containerFeedGeral');

		//pre carregando o gif
		loading = new Image(); loading.src = 'loading.gif';
		$('#menu-time a').live('click', function( e ){
			e.preventDefault();
			content.html( '<img style="margin: 35% 42%" src="../static/imagens/loading.gif" />' );

			var href = $( this ).attr('href');
			$.ajax({
				url: href,
				success: function( response ){
					//forçando o parser
					var data = $( '<div>'+response+'</div>' ).find('#containerFeedGeral').html();

					//apenas atrasando a troca, para mostrarmos o loading
					window.setTimeout( function(){
						content.fadeOut('slow', function(){
							content.html( data ).fadeIn();
						});
					}, 0 );
				}
			});

		});
	});
	
		