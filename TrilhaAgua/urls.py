from django.conf.urls import patterns, include, url
from django.contrib import admin
from django.conf.urls.static import static
from TrilhaAgua import settings
admin.autodiscover()

urlpatterns = patterns('',
    
    url(r'^admin/', include(admin.site.urls)),
    
    url (r'^$', 'RedeSocial.views.index.Login'),
    url (r'^login$', 'RedeSocial.views.index.Login'),
    url (r'^verificar$', 'RedeSocial.views.index.Verificar'),
    url (r'^cadastro$', 'RedeSocial.views.index.Cadastro'),
    url (r'^cadastrar$', 'RedeSocial.views.index.Cadastrar'),
    url (r'^timeline$', 'RedeSocial.views.index.Timeline'),
    url (r'^feed$', 'RedeSocial.views.index.Feed'),
    url (r'^time_amigos$', 'RedeSocial.views.index.Timeline_amigos'),
    url (r'^time_turma$', 'RedeSocial.views.index.Timeline_turma'),
    url (r'^perfil$', 'RedeSocial.views.index.Perfil'),
    url (r'^postar$', 'RedeSocial.views.index.Postar'),
    url (r'^postarComentarios$', 'RedeSocial.views.index.PostarComentario'),
    url (r'^postarComentarios2$', 'RedeSocial.views.index.PostarComentario2'),
    url (r'^editarPerfil$', 'RedeSocial.views.index.editarPerfil'),
    url (r'^pergunta$', 'RedeSocial.views.index.Pergunta'),
    url (r'^verificarPergunta$', 'RedeSocial.views.index.VerificarPergunta'),
    url (r'^redefinirsenha$', 'RedeSocial.views.index.Redefinir'),
    url (r'^atualizarInformacoes$', 'RedeSocial.views.index.AtualizarInformacoes'),
    url (r'^buscaPerfilUsuario$', 'RedeSocial.views.index.BuscaPerfilUsuario'),
    url (r'^logout$', 'RedeSocial.views.index.Logout'),
    url (r'^visualizarComentarios$', 'RedeSocial.views.index.VisualizarComentarios'),
    
    
    url (r'^desafiar$', 'RedeSocial.views.index.Desafiar'),
    url (r'^ativos$', 'RedeSocial.views.index.Ativos'),
    url (r'^pendentes$', 'RedeSocial.views.index.Pendentes'),
    url (r'^cumpridos$', 'RedeSocial.views.index.Cumpridos'),
    
    
    url (r'^rankings$', 'RedeSocial.views.index.Rankings'),
    url (r'^rankings_geral$', 'RedeSocial.views.index.Rankings_Geral'),
    url (r'^rankings_turma$', 'RedeSocial.views.index.Rankings_Turma'),
    url (r'^rankings_amigos$', 'RedeSocial.views.index.Rankings_Amigos'),
    url (r'^campeoes$', 'RedeSocial.views.index.Campeoes'),
    url (r'^conquistas$', 'RedeSocial.views.index.Conquistas'),
    url (r'^amigos$', 'RedeSocial.views.index.Tela_Amigos'),
    url (r'^sobre$', 'RedeSocial.views.index.Sobre'),
    url (r'^pesquisa$', 'RedeSocial.views.index.Pesquisa'),
    url (r'^fazer_amizade$', 'RedeSocial.views.index.Fazer_Amizade'),
    url (r'^pedido_Solicitacao$', 'RedeSocial.views.index.Pedido_Solicitacao'),
    url (r'^lancar_desafios$', 'RedeSocial.views.index.Lancar_Desafios'),
    url (r'^pedido_desafio$', 'RedeSocial.views.index.Pedido_Desafio'),
    url (r'^cumprir_desafio$', 'RedeSocial.views.index.Cumprir_Desafio'),
    url (r'^postar_desafio$', 'RedeSocial.views.index.Postar_Desafio'),
    url (r'^lancar_desafio$', 'RedeSocial.views.index.Lancar_Desafio'),
    url (r'^lancar_desafios_turma$', 'RedeSocial.views.index.Lancar_Desafio_Turma'),
    url (r'^verificar_desafio$', 'RedeSocial.views.index.Verificar_Desafio'),
    url (r'^atribuir_desafio$', 'RedeSocial.views.index.Atribuir_Desafio'),
    url (r'^desafiar_amigo$', 'RedeSocial.views.index.Desafiar_Amigo'),
    url (r'^mensagens$', 'RedeSocial.views.index.Mensagens_Usuario'),
    url (r'^apagar_mensagem$', 'RedeSocial.views.index.Apagar_Menagem'),
    url (r'^base$', 'RedeSocial.views.index.Base'),
    url (r'^hello$', 'RedeSocial.views.index.hello'),
    url (r'^apagar_postagem$', 'RedeSocial.views.index.Apagar_Post'),
    url (r'^apagar_comentario$', 'RedeSocial.views.index.Apagar_Comentario'),
    url (r'^Atribuir_Conquista$', 'RedeSocial.views.index.Atribuir_Conquistas'),
     
    url (r'^pingo$', 'RedeSocial.views.index.Pingo_Like'),
    url (r'^despingo$', 'RedeSocial.views.index.Despingo_Deslike'),
    url (r'^usuarios_curtiram$', 'RedeSocial.views.index.Usuarios_curtiram'),
    
    url (r'^mais_posts$', 'RedeSocial.views.index.Mais_posts'),
    url (r'^descurtir$', 'RedeSocial.views.index.Descurtir'),
    url (r'^curtir$', 'RedeSocial.views.index.Curtir'),
    
) + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)


