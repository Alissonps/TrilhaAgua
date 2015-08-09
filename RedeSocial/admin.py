from django.contrib import admin
from RedeSocial.models import Usuario, TimeLine, Comentarios, Solicitacao, \
    Amigos, Solicitacao_Desafio, Desafio, Desafio_Ativo, \
    Beta_TimeLine, Mensagens, Competicao, Campeao, hist_pontuacao, Pingo, \
    Conquista, Insignia, Usu_Comp_Semanal, LEL, HBG, TS1S2, SS1S2, Conq_menino_menina

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
admin.site.register(Mensagens)
admin.site.register(Competicao)
admin.site.register(Campeao)
admin.site.register(hist_pontuacao)
admin.site.register(Pingo)
admin.site.register(Insignia)
admin.site.register(Conquista)
admin.site.register(Usu_Comp_Semanal)
admin.site.register(LEL)
admin.site.register(HBG)
admin.site.register(TS1S2)
admin.site.register(SS1S2)
admin.site.register(Conq_menino_menina)
