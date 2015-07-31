$(document).ready(function(){
		
$("#geral").live('click', function(){
			$("#containerAmigos").load("rankings_geral");
		});
		
		$("#amigos").live('click', function(){
			$("#containerAmigos").load("rankings_amigos");
		});
		
		$("#turma").live('click', function(){
			$("#containerAmigos").load("rankings_turma");
		});
		
});			
		/*$(document).ready(function() {
			$("#geral").live('click', function(){
				$('#containerAmigos').load('rankings_turma', 
					function(){
						$("table tr:odd").css("background", "green");
					}
				
			);
			});
		});/*
		