from django.contrib import admin
from RedeSocial.models import Usuario, TimeLine, Comentarios, Solicitacao, \
    Amigos, Solicitacao_Desafio, Desafio, Desafio_Ativo, Cont_Postagem, \
    Beta_TimeLine, Mensagens, Competicao, Campeao, hist_pontuacao, Pingo, \
    Conquista, Insignia

admin.site.register(Usuario)

class AdminBlog(admin.ModelAdmin):
    pass

admin.site.register(TimeLine, AdminBlog)
admin.site.register(Beta_TimeLine, AdminBlog)
admin.site.register(Comentarios)
admin.site.register(Solicitacao)
admin.site.register(Amigos)
admin.site.register(Solicitacao_Desafio)
admin.site.register(Desafio)
admin.site.register(Desafio_Ativo)
admin.site.register(Cont_Postagem)
admin.site.register(Mensagens)
admin.site.register(Competicao)
admin.site.register(Campeao)
admin.site.register(hist_pontuacao)
admin.site.register(Pingo)
admin.site.register(Insignia)
admin.site.register(Conquista)
