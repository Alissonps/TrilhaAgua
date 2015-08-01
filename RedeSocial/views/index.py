# -*- coding:utf8 -*-

from django.shortcuts import render, render_to_response
from django.http.response import HttpResponse
from django.views.decorators.csrf import csrf_exempt
from _winapi import NULL
from RedeSocial.models import Usuario, TimeLine, Comentarios, Amigos, \
    Solicitacao, Desafio, Solicitacao_Desafio, Desafio_Ativo, Cont_Postagem,\
    Beta_TimeLine, Mensagens, Competicao, Campeao, hist_pontuacao, Pingo, \
    Insignia, Conquista, Usu_Comp_Semanal
from datetime import datetime, date, timedelta
from django.utils import timezone


            
def hello(request):
    return HttpResponse('Hello World!')

def Base(request):
    return render(request, 'en/public/Base.HTML')

def Construcao (request):
    u = Usuario.objects.filter(login=request.session['id']).get()
    slct = Solicitacao.objects.filter(amigo=u)
    qtd_solicitacoes = len(slct)
    
    return render(request, 'en/public/Construcao.HTML', {"qtd_solicitacoes": qtd_solicitacoes, "Usuario":u})

def Tela_Amigos (request):
    #---------------------------Notificações-----------------------------------------------------
    #Sessão do usuario
    u = Usuario.objects.filter(login=request.session['id']).get()
    #Quantidade de solicitações de amizade
    slct = Solicitacao.objects.filter(amigo=u)
    qtd_solicitacoes = len(slct)
    #Solicitações de desafios
    soli_desafios = Solicitacao_Desafio.objects.filter(usuario_desafiado = u)
    qtd_soli_desafios = len(soli_desafios)
    #Desafios Ativos
    d_ativos_desafiado = Desafio_Ativo.objects.filter(usuario_desafiado = u)
    #Desafios Cumpridos
    d_ativos_desafiante = Desafio_Ativo.objects.filter(usuario_desafiante = u, cumprido = True)
    qtd_d_cumpridos = len(d_ativos_desafiante)
    #Quantidade de Mensagens
    msgs = Mensagens.objects.filter(usuario = u)
    qtd_msgs = len(msgs)
    #{"desafios_cumpridos": qtd_d_cumpridos,"soli_desafios":qtd_soli_desafios, "d_ativos_desafiado":d_ativos_desafiado,"Usuario":u, "qtd_solicitacoes": qtd_solicitacoes}
    #----------------------------------------------------------------------------------------------
    
    qtd_d_ativos_desafiado = len(d_ativos_desafiado)
    ranking_geral = Usuario.objects.all().order_by('-pontos')
    lista_geral = list(ranking_geral)
    pos_geral = lista_geral.index(u) + 1
    
    ranking_turma = Usuario.objects.filter(turma = u.turma).order_by('-pontos')
    lista_turma = list(ranking_turma)
    pos_turma = lista_turma.index(u) + 1
    
    
    meusAmigos = Amigos.objects.filter(dono=u)
    minhas_Solicitacoes = Solicitacao.objects.filter(amigo=u)
    
    return render(request, 'en/public/Tela_Amigos.HTML', {"qtd_msgs": qtd_msgs, "Meus": meusAmigos, "Minhas_Solicitacoes": minhas_Solicitacoes, "desafios_cumpridos": qtd_d_cumpridos,"soli_desafios":qtd_soli_desafios, "d_ativos_desafiado":d_ativos_desafiado,"Usuario":u, "qtd_solicitacoes": qtd_solicitacoes, "qtd_d_ativos_desafiado": qtd_d_ativos_desafiado,"pos_turma": pos_turma, "pos_geral": pos_geral,"qtd_msgs": qtd_msgs, "desafios_cumpridos": qtd_d_cumpridos,"soli_desafios":qtd_soli_desafios, "d_ativos_desafiado":d_ativos_desafiado, "qtd_solicitacoes": qtd_solicitacoes})

def Login (request):
    return render(request, 'en/public/Login.HTML')

@csrf_exempt
def Postar (request):
    Texto = request.POST.get('mensagem', False)
    Foto = request.FILES.get('arquivo', False)
        
    competicao_atual = Competicao.objects.filter(ativo = True).get()
        
    qtd_post = TimeLine.objects.all()
    add_post = len(qtd_post) + 1

    u = Usuario.objects.filter(login=request.session['id']).get()

    passar = False
        
    if(Texto != False and Foto != False):
        time = TimeLine(text=Texto, usuario=u, foto=Foto, competicao = competicao_atual)
        time.save()
        
        cont_post = Cont_Postagem.objects.filter(id = 1).get()
        cont_post.qtd = add_post
        cont_post.save()
        
        passar = True
        
    elif(Texto != False):
        time = TimeLine(text=Texto, usuario=u, foto=Foto, competicao = competicao_atual)
        time.save()
        
        cont_post = Cont_Postagem.objects.filter(id = 1).get()
        cont_post.qtd = add_post   
        cont_post.save()
        
        passar = True
        
    else:
        passar = True
        
    if(passar == True): 
        return Timeline(request) 
    

@csrf_exempt
def PostarComentario (request):
    Texto = request.POST['cComentario']
    Id = request.POST['cId']
    
    u = Usuario.objects.filter(login=request.session['id']).get()
   
    Postagem = TimeLine.objects.filter(id=Id).get()
        
    comentario = Comentarios(text=Texto, usuario=u, postagem=Postagem)
    comentario.save()
    
    coments = Comentarios.objects.filter(postagem=Postagem)      
    cont = len(coments)
    
    Postagem.qtd_coments = cont
    Postagem.save()
    
    entries = TimeLine.objects.all().order_by('-date')
    
    return HttpResponse(Postagem.qtd_coments)

    
    
def Timeline (request):
    u = Usuario.objects.filter(login=request.session['id']).get()
    
    qtd_entries = []
    
    #Postagens
    entries = TimeLine.objects.all().order_by('-date') 
        
    pingo = Pingo.objects.all()
    
    i = 0
    for a in entries:
              
        try:
            pingo = Pingo.objects.filter(usuario = u, postagem = a).get()
            a.curtiu = True
            a.save()
        except:
            a.curtiu = False       
            a.save()
        
        qtd_entries.append(a)
        
        i = i + 1
    
        if (i == 3):
            break

    
    #---------------------------Notificações-----------------------------------------------------
    #Sessão do usuario
    
    #Quantidade de solicitações de amizade
    slct = Solicitacao.objects.filter(amigo=u)
    qtd_solicitacoes = len(slct)
    #Solicitações de desafios
    soli_desafios = Solicitacao_Desafio.objects.filter(usuario_desafiado = u)
    qtd_soli_desafios = len(soli_desafios)
    #Desafios Ativos
    d_ativos_desafiado = Desafio_Ativo.objects.filter(usuario_desafiado = u)
    qtd_d_ativos_desafiado = len(d_ativos_desafiado)
    #Desafios Cumpridos
    d_ativos_desafiante = Desafio_Ativo.objects.filter(usuario_desafiante = u, cumprido = True)
    qtd_d_cumpridos = len(d_ativos_desafiante)
    #Quantidade de Mensagens
    msgs = Mensagens.objects.filter(usuario = u)
    qtd_msgs = len(msgs)
    
    #----------------------------------------------------------------------------------------------

    qtd_d_ativos_desafiado = len(d_ativos_desafiado)
    ranking_geral = Usuario.objects.all().order_by('-pontos')
    lista_geral = list(ranking_geral)
    pos_geral = lista_geral.index(u) + 1
    
    ranking_turma = Usuario.objects.filter(turma = u.turma).order_by('-pontos')
    lista_turma = list(ranking_turma)
    pos_turma = lista_turma.index(u) + 1
                
    return render_to_response('en/public/Timeline.HTML', {"entries": qtd_entries, "qtd_d_ativos_desafiado": qtd_d_ativos_desafiado,"pos_turma": pos_turma, "pos_geral": pos_geral,"qtd_msgs": qtd_msgs, "desafios_cumpridos": qtd_d_cumpridos,"soli_desafios":qtd_soli_desafios, "d_ativos_desafiado":d_ativos_desafiado, "Usuario":u, "qtd_solicitacoes": qtd_solicitacoes})

def Feed (request):
    u = Usuario.objects.filter(login=request.session['id']).get()
    
    entries = TimeLine.objects.all().order_by('-date')
    
    qtd_entries = []
    
    i = 0
    for a in entries:
              
        try:
            pingo = Pingo.objects.filter(usuario = u, postagem = a).get()
            a.curtiu = True
            a.save()
        except:
            a.curtiu = False       
            a.save()
        
        qtd_entries.append(a)
        
        i = i + 1
    
        if (i == 3):
            break
        
    return render_to_response('en/public/Feeds2.HTML', {"entries": qtd_entries, "Usuario":u})

def Timeline_turma (request):
    u = Usuario.objects.filter(login=request.session['id']).get()
    
    turma = Usuario.objects.filter(turma = u.turma)
    entries = TimeLine.objects.filter(usuario = turma).order_by('-date')
    pingo = Pingo.objects.all()
    
    for e in entries:
        try:
            pingo = Pingo.objects.filter(usuario = u, postagem = e).get()
            e.curtiu = True
            e.save()
        except:
            e.curtiu = False       
            e.save() 
            
     #---------------------------Notificações-----------------------------------------------------
    #Sessão do usuario
    
    #Quantidade de solicitações de amizade
    slct = Solicitacao.objects.filter(amigo=u)
    qtd_solicitacoes = len(slct)
    #Solicitações de desafios
    soli_desafios = Solicitacao_Desafio.objects.filter(usuario_desafiado = u)
    qtd_soli_desafios = len(soli_desafios)
    #Desafios Ativos
    d_ativos_desafiado = Desafio_Ativo.objects.filter(usuario_desafiado = u)
    qtd_d_ativos_desafiado = len(d_ativos_desafiado)
    #Desafios Cumpridos
    d_ativos_desafiante = Desafio_Ativo.objects.filter(usuario_desafiante = u, cumprido = True)
    qtd_d_cumpridos = len(d_ativos_desafiante)
    #Quantidade de Mensagens
    msgs = Mensagens.objects.filter(usuario = u)
    qtd_msgs = len(msgs)
    
    #----------------------------------------------------------------------------------------------

    qtd_d_ativos_desafiado = len(d_ativos_desafiado)
    ranking_geral = Usuario.objects.all().order_by('-pontos')
    lista_geral = list(ranking_geral)
    pos_geral = lista_geral.index(u) + 1
    
    ranking_turma = Usuario.objects.filter(turma = u.turma).order_by('-pontos')
    lista_turma = list(ranking_turma)
    pos_turma = lista_turma.index(u) + 1
    
    return render_to_response('en/public/Timeline_turma.HTML', {"entries": entries, "Usuario":u, "qtd_d_ativos_desafiado": qtd_d_ativos_desafiado,"pos_turma": pos_turma, "pos_geral": pos_geral,"qtd_msgs": qtd_msgs, "desafios_cumpridos": qtd_d_cumpridos,"soli_desafios":qtd_soli_desafios, "d_ativos_desafiado":d_ativos_desafiado, "qtd_solicitacoes": qtd_solicitacoes})

def Timeline_amigos (request):
    u = Usuario.objects.filter(login=request.session['id']).get()
   
    #Postagens
    pesquisa_amigos = Amigos.objects.filter(dono=u)
    entries = TimeLine.objects.all().order_by('-date')
    pingo = Pingo.objects.all()
    
    for e in entries:
        try:
            pingo = Pingo.objects.filter(usuario = u, postagem = e).get()
            e.curtiu = True
            e.save()
        except:
            e.curtiu = False       
            e.save()
            
    amigos = []
    posts_amigos = []
    
    for a in pesquisa_amigos:
        amigos.append(a.amigo)
        
    for a in entries:    
        if a.usuario in amigos:
            posts_amigos.append(a)  
    
    #---------------------------Notificações-----------------------------------------------------
    #Sessão do usuario
    
    #Quantidade de solicitações de amizade
    slct = Solicitacao.objects.filter(amigo=u)
    qtd_solicitacoes = len(slct)
    #Solicitações de desafios
    soli_desafios = Solicitacao_Desafio.objects.filter(usuario_desafiado = u)
    qtd_soli_desafios = len(soli_desafios)
    #Desafios Ativos
    d_ativos_desafiado = Desafio_Ativo.objects.filter(usuario_desafiado = u)
    qtd_d_ativos_desafiado = len(d_ativos_desafiado)
    #Desafios Cumpridos
    d_ativos_desafiante = Desafio_Ativo.objects.filter(usuario_desafiante = u, cumprido = True)
    qtd_d_cumpridos = len(d_ativos_desafiante)
    #Quantidade de Mensagens
    msgs = Mensagens.objects.filter(usuario = u)
    qtd_msgs = len(msgs)
    
    #----------------------------------------------------------------------------------------------

    qtd_d_ativos_desafiado = len(d_ativos_desafiado)
    ranking_geral = Usuario.objects.all().order_by('-pontos')
    lista_geral = list(ranking_geral)
    pos_geral = lista_geral.index(u) + 1
    
    ranking_turma = Usuario.objects.filter(turma = u.turma).order_by('-pontos')
    lista_turma = list(ranking_turma)
    pos_turma = lista_turma.index(u) + 1
    #"qtd_d_ativos_desafiado": qtd_d_ativos_desafiado,"pos_turma": pos_turma, "pos_geral": pos_geral,"qtd_msgs": qtd_msgs, "desafios_cumpridos": qtd_d_cumpridos,"soli_desafios":qtd_soli_desafios, "d_ativos_desafiado":d_ativos_desafiado, "qtd_solicitacoes": qtd_solicitacoes
    
    return render_to_response('en/public/Timeline_amigos.HTML', {"entries": posts_amigos, "Usuario":u, "qtd_d_ativos_desafiado": qtd_d_ativos_desafiado,"pos_turma": pos_turma, "pos_geral": pos_geral,"qtd_msgs": qtd_msgs, "desafios_cumpridos": qtd_d_cumpridos,"soli_desafios":qtd_soli_desafios, "d_ativos_desafiado":d_ativos_desafiado, "qtd_solicitacoes": qtd_solicitacoes})

@csrf_exempt  
def Apagar_Post (request):
    u = Usuario.objects.filter(login=request.session['id']).get()
    
    id_post = request.POST['id']
    postagem = TimeLine.objects.filter(id = id_post).get()
    postagem.delete()
    
    return Timeline(request)

@csrf_exempt  
def Apagar_Comentario (request):
    u = Usuario.objects.filter(login=request.session['id']).get()
    
    id_coment = request.POST.get('id', False)
    id_post = request.POST.get('id_postagem', False)
    
    comentario = Comentarios.objects.filter(pk = id_coment).get()
    comentario.delete()
    
    postagem = TimeLine.objects.filter(id = id_post).get()
    postagem.qtd_coments = postagem.qtd_coments - 1
    postagem.save() 
    
    return Timeline(request)

@csrf_exempt
def Verificar (request):
        LOGIN = request.POST['Login']
        SENHA = request.POST['Senha']
        mensagem = " "
        
        try:
            request.session['id'] = request.POST['Login'] 
            
            u = Usuario.objects.filter(login=request.session['id']).get()
           
            if(LOGIN == u.login and SENHA == u.senha):
                
                try:
                    
                    cs = Usu_Comp_Semanal.objects.filter(usuario = u, ativo = True).get()
                
                    data_atual = timezone.now()
                        
                    if(cs.data_fim < data_atual):
                    
                        cs.data_fim = cs.data_fim + timedelta(days = 7) 
                        cs.save()
                
                except:
                    
                    data_atual = timezone.now()
                     
                    data_f = data_atual + timedelta(days = 7) 
                        
                    cs = Usu_Comp_Semanal(data_inicio = data_atual, data_fim = data_f, usuario = u, qtd_desafios = 0, ativo = True)
                    cs.save()               
                
                return Timeline(request)
            
            else:
                mensagem = "Dados incorretos!"
                return render(request, 'en/public/Login.HTML', {"msg": mensagem})

        except:
            mensagem = "Dados incorretos!"
            return render(request, 'en/public/Login.HTML', {"msg": mensagem})

def Cadastro (request):
    return render(request, 'en/public/Cadastro.HTML')

@csrf_exempt
def Cadastrar (request):
    Login = request.POST.get('cLogin', False)
    Senha = request.POST.get('cSenha', False)
    Nome = request.POST.get('cNome', False)
    Email = request.POST.get('cEmail', False)
    Matricula = request.POST.get('cMatricula', False)
    Idade = request.POST.get('cIdade', False)
    Turma = request.POST.get('cTurma', False)
    Sexo = request.POST.get('cSexo', False)
    Pergunta = request.POST.get('cPergunta', False)
    Resposta = request.POST.get('cResposta', False)
    Descricao = " "
    Foto = request.POST['cFoto']
    
    mensagem = " "
    ast = " "
    
    try:
        existe = Usuario.objects.filter(login=Login).get()
        if(existe.login == Login):
            mensagem = "Login de usuario já existe!"
            ast = "*"
            return render(request, 'en/public/Cadastro.HTML' , {"msg2": mensagem, "ast": ast})  
    except:
        usuario = Usuario(login=Login, senha=Senha, nome=Nome, email=Email, matricula=Matricula, idade=Idade, turma=Turma, sexo=Sexo, pergunta=Pergunta, resposta=Resposta, descricao=Descricao, foto=Foto, professor = False)
        if(Login != False and Senha != False and Nome != False and Email != False and Matricula != False  and Idade != False  and Turma != False and Sexo != False):
            usuario.save()
            mensagem = "Usuario cadastrado!"
            return render(request, 'en/public/Login.HTML', {"msg": mensagem})
        else:
            mensagem = "Preencha os campos!"
            return render(request, 'en/public/Cadastro.HTML' , {"msg2": mensagem})

def editarPerfil (request):
        
        #---------------------------Notificações-----------------------------------------------------
        #Sessão do usuario
        u = Usuario.objects.filter(login=request.session['id']).get()
        #Quantidade de solicitações de amizade
        slct = Solicitacao.objects.filter(amigo=u)
        qtd_solicitacoes = len(slct)
        #Solicitações de desafios
        soli_desafios = Solicitacao_Desafio.objects.filter(usuario_desafiado = u)
        qtd_soli_desafios = len(soli_desafios)
        #Desafios Ativos
        d_ativos_desafiado = Desafio_Ativo.objects.filter(usuario_desafiado = u)
        #Desafios Cumpridos
        d_ativos_desafiante = Desafio_Ativo.objects.filter(usuario_desafiante = u, cumprido = True)
        qtd_d_cumpridos = len(d_ativos_desafiante)
        #Quantidade de Mensagens
        msgs = Mensagens.objects.filter(usuario = u)
        qtd_msgs = len(msgs)
        #{"desafios_cumpridos": qtd_d_cumpridos,"soli_desafios":qtd_soli_desafios, "d_ativos_desafiado":d_ativos_desafiado,"Usuario":u, "qtd_solicitacoes": qtd_solicitacoes}
        #----------------------------------------------------------------------------------------------
        
        qtd_d_ativos_desafiado = len(d_ativos_desafiado)
        ranking_geral = Usuario.objects.all().order_by('-pontos')
        lista_geral = list(ranking_geral)
        pos_geral = lista_geral.index(u) + 1    
    
        ranking_turma = Usuario.objects.filter(turma = u.turma).order_by('-pontos')
        lista_turma = list(ranking_turma)
        pos_turma = lista_turma.index(u) + 1
        #"qtd_d_ativos_desafiado": qtd_d_ativos_desafiado,"pos_turma": pos_turma, "pos_geral": pos_geral,"qtd_msgs": qtd_msgs, "desafios_cumpridos": qtd_d_cumpridos,"soli_desafios":qtd_soli_desafios, "d_ativos_desafiado":d_ativos_desafiado, "qtd_solicitacoes": qtd_solicitacoes
    
        return render(request, 'en/public/EditarPerfil.HTML', {"qtd_msgs": qtd_msgs,"desafios_cumpridos": qtd_d_cumpridos,"soli_desafios":qtd_soli_desafios, "d_ativos_desafiado":d_ativos_desafiado,"Usuario":u, "qtd_solicitacoes": qtd_solicitacoes, "qtd_d_ativos_desafiado": qtd_d_ativos_desafiado,"pos_turma": pos_turma, "pos_geral": pos_geral,"qtd_msgs": qtd_msgs, "desafios_cumpridos": qtd_d_cumpridos,"soli_desafios":qtd_soli_desafios, "d_ativos_desafiado":d_ativos_desafiado, "qtd_solicitacoes": qtd_solicitacoes})
    
def Perfil (request):
        #---------------------------Notificações-----------------------------------------------------
        #Sessão do usuario
    
        u = Usuario.objects.filter(login=request.session['id']).get()
        #Quantidade de solicitações de amizade
        slct = Solicitacao.objects.filter(amigo=u)
        qtd_solicitacoes = len(slct)
        #Solicitações de desafios
        soli_desafios = Solicitacao_Desafio.objects.filter(usuario_desafiado = u)
        qtd_soli_desafios = len(soli_desafios)
        #Desafios Ativos
        d_ativos_desafiado = Desafio_Ativo.objects.filter(usuario_desafiado = u)
        #Desafios Cumpridos
        d_ativos_desafiante = Desafio_Ativo.objects.filter(usuario_desafiante = u, cumprido = True)
        qtd_d_cumpridos = len(d_ativos_desafiante)
        #Quantidade de Mensagens
        msgs = Mensagens.objects.filter(usuario = u)
        qtd_msgs = len(msgs)
        #{"desafios_cumpridos": qtd_d_cumpridos,"soli_desafios":qtd_soli_desafios, "d_ativos_desafiado":d_ativos_desafiado,"Usuario":u, "qtd_solicitacoes": qtd_solicitacoes}
        #----------------------------------------------------------------------------------------------
        
        qtd_d_ativos_desafiado = len(d_ativos_desafiado)
        ranking_geral = Usuario.objects.all().order_by('-pontos')
        lista_geral = list(ranking_geral)
        pos_geral = lista_geral.index(u) + 1    
    
        ranking_turma = Usuario.objects.filter(turma = u.turma).order_by('-pontos')
        lista_turma = list(ranking_turma)
        pos_turma = lista_turma.index(u) + 1
        #"qtd_d_ativos_desafiado": qtd_d_ativos_desafiado,"pos_turma": pos_turma, "pos_geral": pos_geral,"qtd_msgs": qtd_msgs, "desafios_cumpridos": qtd_d_cumpridos,"soli_desafios":qtd_soli_desafios, "d_ativos_desafiado":d_ativos_desafiado, "qtd_solicitacoes": qtd_solicitacoes
        
        if(u.login != NULL):
            return render(request, 'en/public/Perfil.HTML', {"qtd_msgs":qtd_msgs,"desafios_cumpridos": qtd_d_cumpridos,"soli_desafios":qtd_soli_desafios, "d_ativos_desafiado":d_ativos_desafiado,"Usuario":u, "qtd_solicitacoes": qtd_solicitacoes, "qtd_d_ativos_desafiado": qtd_d_ativos_desafiado,"pos_turma": pos_turma, "pos_geral": pos_geral,"qtd_msgs": qtd_msgs, "desafios_cumpridos": qtd_d_cumpridos,"soli_desafios":qtd_soli_desafios, "d_ativos_desafiado":d_ativos_desafiado, "qtd_solicitacoes": qtd_solicitacoes, "qtd_d_ativos_desafiado": qtd_d_ativos_desafiado,"pos_turma": pos_turma, "pos_geral": pos_geral,"qtd_msgs": qtd_msgs, "desafios_cumpridos": qtd_d_cumpridos,"soli_desafios":qtd_soli_desafios, "d_ativos_desafiado":d_ativos_desafiado, "qtd_solicitacoes": qtd_solicitacoes})
        else:
            return HttpResponse('Você não está logado')

def AtualizarInformacoes(request):
    
    novoNome = request.POST.get('eNome', False)
    novaIdade = request.POST.get('eIdade', False)
    novaTurma = request.POST.get('eTurma', False)
    novaDescricao = request.POST.get('eDescricao', False)
    Foto = request.FILES.get('arquivo', False)
    
    #---------------------------Notificações-----------------------------------------------------
    #Sessão do usuario
    u = Usuario.objects.filter(login=request.session['id']).get()
    #Quantidade de solicitações de amizade
    slct = Solicitacao.objects.filter(amigo=u)
    qtd_solicitacoes = len(slct)
    #Solicitações de desafios
    soli_desafios = Solicitacao_Desafio.objects.filter(usuario_desafiado = u)
    qtd_soli_desafios = len(soli_desafios)
    #Desafios Ativos
    d_ativos_desafiado = Desafio_Ativo.objects.filter(usuario_desafiado = u)
    #Desafios Cumpridos
    d_ativos_desafiante = Desafio_Ativo.objects.filter(usuario_desafiante = u, cumprido = True)
    qtd_d_cumpridos = len(d_ativos_desafiante)
    #Quantidade de Mensagens
    msgs = Mensagens.objects.filter(usuario = u)
    qtd_msgs = len(msgs)
    #{"desafios_cumpridos": qtd_d_cumpridos,"soli_desafios":qtd_soli_desafios, "d_ativos_desafiado":d_ativos_desafiado,"Usuario":u, "qtd_solicitacoes": qtd_solicitacoes}
    #----------------------------------------------------------------------------------------------
    
    qtd_d_ativos_desafiado = len(d_ativos_desafiado)
    ranking_geral = Usuario.objects.all().order_by('-pontos')
    lista_geral = list(ranking_geral)
    pos_geral = lista_geral.index(u) + 1    
    
    ranking_turma = Usuario.objects.filter(turma = u.turma).order_by('-pontos')
    lista_turma = list(ranking_turma)
    pos_turma = lista_turma.index(u) + 1
    #"qtd_d_ativos_desafiado": qtd_d_ativos_desafiado,"pos_turma": pos_turma, "pos_geral": pos_geral,"qtd_msgs": qtd_msgs, "desafios_cumpridos": qtd_d_cumpridos,"soli_desafios":qtd_soli_desafios, "d_ativos_desafiado":d_ativos_desafiado, "qtd_solicitacoes": qtd_solicitacoes
    
    if(novoNome != False):
        u.nome = novoNome
    else:
        u.nome = u.nome
    if(novaIdade != False):
        u.idade = novaIdade
    else:
        u.idade = u.idade
    if(novaTurma != False):
        u.turma = novaTurma
    else:
        u.turma = u.turma
    if(novaDescricao != False):
        u.descricao = novaDescricao
    else:
        u.descricao = u.descricao
    if(Foto != False):
        u.foto = Foto
    else:
        u.foto = u.foto
        
    
    request.session['id'] = u.login  
    u.save()
    return render(request, 'en/public/Perfil.HTML', {"qtd_msgs":qtd_msgs,"desafios_cumpridos": qtd_d_cumpridos,"soli_desafios":qtd_soli_desafios, "d_ativos_desafiado":d_ativos_desafiado,"Usuario":u, "qtd_solicitacoes": qtd_solicitacoes,"qtd_d_ativos_desafiado": qtd_d_ativos_desafiado,"pos_turma": pos_turma, "pos_geral": pos_geral,"qtd_msgs": qtd_msgs, "desafios_cumpridos": qtd_d_cumpridos,"soli_desafios":qtd_soli_desafios, "d_ativos_desafiado":d_ativos_desafiado, "qtd_solicitacoes": qtd_solicitacoes})

def Pergunta(request):
    return render(request, 'en/public/Pergunta.HTML')
    
    
def VerificarPergunta (request):
    Login = request.POST.get('cLogin', False)
    Pergunta = request.POST.get('cPergunta', False)
    Resposta = request.POST.get('cResposta', False)
    
    u = Usuario.objects.filter(login=Login, pergunta=Pergunta).get()
    mensagem = ''
    
    if(u.resposta == Resposta and u.pergunta == Pergunta):

        return render(request, 'en/public/RedefinirSenha.HTML')
    else:
        mensagem = 'Dados incorretos!'
        return render(request, 'en/public/Pergunta.HTML', {"msg": mensagem})
    
 
@csrf_exempt   
def Redefinir(request):
    
    Login = request.POST.get('cLogin', False)
    novaSenha = request.POST.get('mSenha', False)
    confirmarSenha = request.POST.get('cmSenha', False)
    mensagem = " "
    
    u = Usuario.objects.filter(login=Login).get()
    
    if(confirmarSenha == novaSenha and confirmarSenha != False):
        u.senha = novaSenha 
        u.save()
        mensagem = 'Senha redefinida com sucesso.'
        return render(request, 'en/public/RedefinirSenha.HTML', {"msg1": mensagem})
    elif(confirmarSenha != novaSenha and confirmarSenha != False):
        mensagem = 'Os dados estão incorretos'
        return render(request, 'en/public/RedefinirSenha.HTML', {"msg2": mensagem})
    else:
        return render(request, 'en/public/RedefinirSenha.HTML')

@csrf_exempt  
def BuscaPerfilUsuario (request):
    
    ID_Usuario = request.POST.get('cUsuario')
    UsuarioBuscado = Usuario.objects.filter(id=ID_Usuario).get()
    
    ranking_turma = Usuario.objects.filter(turma = UsuarioBuscado.turma).order_by('-pontos')
    lista_turma = list(ranking_turma)
    pos_turma_u = lista_turma.index(UsuarioBuscado) + 1
    
    ranking_geral = Usuario.objects.all().order_by('-pontos')
    lista_geral = list(ranking_geral)
    pos_geral_u = lista_geral.index(UsuarioBuscado) + 1 
    
    conquista = Conquista.objects.filter(usuario = UsuarioBuscado)
    
    #---------------------------Notificações-----------------------------------------------------
    #Sessão do usuario
    u = Usuario.objects.filter(login=request.session['id']).get()
    #Quantidade de solicitações de amizade
    slct = Solicitacao.objects.filter(amigo=u)
    qtd_solicitacoes = len(slct)
    #Solicitações de desafios
    soli_desafios = Solicitacao_Desafio.objects.filter(usuario_desafiado = u)
    qtd_soli_desafios = len(soli_desafios)
    #Desafios Ativos
    d_ativos_desafiado = Desafio_Ativo.objects.filter(usuario_desafiado = u)
    qtd_d_ativos_desafiado = len(d_ativos_desafiado)
    #Desafios Cumpridos
    d_ativos_desafiante = Desafio_Ativo.objects.filter(usuario_desafiante = u, cumprido = True)
    qtd_d_cumpridos = len(d_ativos_desafiante)
    #Quantidade de Mensagens
    msgs = Mensagens.objects.filter(usuario = u)
    qtd_msgs = len(msgs)
    #{"desafios_cumpridos": qtd_d_cumpridos,"soli_desafios":qtd_soli_desafios, "d_ativos_desafiado":d_ativos_desafiado,"Usuario":u, "qtd_solicitacoes": qtd_solicitacoes}
    #----------------------------------------------------------------------------------------------
    
    qtd_d_ativos_desafiado = len(d_ativos_desafiado)
    ranking_geral = Usuario.objects.all().order_by('-pontos')
    lista_geral = list(ranking_geral)
    pos_geral = lista_geral.index(u) + 1
    
    ranking_turma = Usuario.objects.filter(turma = u.turma).order_by('-pontos')
    lista_turma = list(ranking_turma)
    pos_turma = lista_turma.index(u) + 1
    #"qtd_d_ativos_desafiado": qtd_d_ativos_desafiado,"pos_turma": pos_turma, "pos_geral": pos_geral,"qtd_msgs": qtd_msgs, "desafios_cumpridos": qtd_d_cumpridos,"soli_desafios":qtd_soli_desafios, "d_ativos_desafiado":d_ativos_desafiado, "qtd_solicitacoes": qtd_solicitacoes
    
    
    return render(request, 'en/public/ConsultaPerfil.HTML' , {"conquista": conquista,"pos_geral_u": pos_geral_u, "pos_turma_u": pos_turma_u, "uBuscado": UsuarioBuscado, "desafios_cumpridos": qtd_d_cumpridos,"soli_desafios":qtd_soli_desafios, "d_ativos_desafiado":d_ativos_desafiado,"Usuario":u, "qtd_solicitacoes": qtd_solicitacoes, "qtd_d_ativos_desafiado": qtd_d_ativos_desafiado,"pos_turma": pos_turma, "pos_geral": pos_geral,"qtd_msgs": qtd_msgs, "desafios_cumpridos": qtd_d_cumpridos,"soli_desafios":qtd_soli_desafios, "d_ativos_desafiado":d_ativos_desafiado, "qtd_solicitacoes": qtd_solicitacoes})
    
def Logout (request):
    try:
        del request.session['id']
    except KeyError:
        pass
    return render(request, 'en/public/Login.HTML')

@csrf_exempt
def VisualizarComentarios (request):
    Id = request.POST['cPost']
    
    Postagem = TimeLine.objects.filter(id=Id).get()
    Coment = Comentarios.objects.filter(postagem=Postagem)
    
    #---------------------------Notificações-----------------------------------------------------
    #Sessão do usuario
    u = Usuario.objects.filter(login=request.session['id']).get()
    #Quantidade de solicitações de amizade
    slct = Solicitacao.objects.filter(amigo=u)
    qtd_solicitacoes = len(slct)
    #Solicitações de desafios
    soli_desafios = Solicitacao_Desafio.objects.filter(usuario_desafiado = u)
    qtd_soli_desafios = len(soli_desafios)
    #Desafios Ativos
    d_ativos_desafiado = Desafio_Ativo.objects.filter(usuario_desafiado = u)
    #Desafios Cumpridos
    d_ativos_desafiante = Desafio_Ativo.objects.filter(usuario_desafiante = u, cumprido = True)
    qtd_d_cumpridos = len(d_ativos_desafiante)
    #Quantidade de Mensagens
    msgs = Mensagens.objects.filter(usuario = u)
    qtd_msgs = len(msgs)
    #{"desafios_cumpridos": qtd_d_cumpridos,"soli_desafios":qtd_soli_desafios, "d_ativos_desafiado":d_ativos_desafiado,"Usuario":u, "qtd_solicitacoes": qtd_solicitacoes}
    #----------------------------------------------------------------------------------------------
    
    return render(request, 'en/public/VisualizarComentarios.HTML', {"qtd_msgs": qtd_msgs,"Postagem": Postagem, "Coment":Coment, "desafios_cumpridos": qtd_d_cumpridos,"soli_desafios":qtd_soli_desafios, "d_ativos_desafiado":d_ativos_desafiado,"Usuario":u, "qtd_solicitacoes": qtd_solicitacoes})

@csrf_exempt
def PostarComentario2 (request):
    Texto = request.POST.get('cComentario', False)
    Id = request.POST['cId']
    
    #---------------------------Notificações-----------------------------------------------------
    #Sessão do usuario
    u = Usuario.objects.filter(login=request.session['id']).get()
    #Quantidade de solicitações de amizade
    slct = Solicitacao.objects.filter(amigo=u)
    qtd_solicitacoes = len(slct)
    #Solicitações de desafios
    soli_desafios = Solicitacao_Desafio.objects.filter(usuario_desafiado = u)
    qtd_soli_desafios = len(soli_desafios)
    #Desafios Ativos
    d_ativos_desafiado = Desafio_Ativo.objects.filter(usuario_desafiado = u)
    #Desafios Cumpridos
    d_ativos_desafiante = Desafio_Ativo.objects.filter(usuario_desafiante = u, cumprido = True)
    qtd_d_cumpridos = len(d_ativos_desafiante)
    #Quantidade de Mensagens
    msgs = Mensagens.objects.filter(usuario = u)
    qtd_msgs = len(msgs)
    #{"desafios_cumpridos": qtd_d_cumpridos,"soli_desafios":qtd_soli_desafios, "d_ativos_desafiado":d_ativos_desafiado,"Usuario":u, "qtd_solicitacoes": qtd_solicitacoes}
    #----------------------------------------------------------------------------------------------
        
    Postagem = TimeLine.objects.filter(id=Id).get()
    
    comentario = Comentarios(text=Texto, usuario=u, postagem=Postagem)
    comentario.save()
    coments = Comentarios.objects.filter(postagem=Postagem)      
    cont = len(coments)
    Postagem.qtd_coments = cont
    Postagem.save()
    
    return render(request, 'en/public/VisualizarComentarios.HTML', {"qtd_msgs":qtd_msgs,"Coment":coments, "Postagem":Postagem, "desafios_cumpridos": qtd_d_cumpridos,"soli_desafios":qtd_soli_desafios, "d_ativos_desafiado":d_ativos_desafiado,"Usuario":u, "qtd_solicitacoes": qtd_solicitacoes})
    
def Sobre (request):
    return render(request, 'en/public/Sobre.HTML')

@csrf_exempt
def Pesquisa (request):
    busca = request.POST['cPesquisar']
    todos = request.POST.get('checkbox_Todos', 'False')
    amigos = request.POST.get('checkbox_Amigos', 'False')
    
    #---------------------------Notificações-----------------------------------------------------
    #Sessão do usuario
    u = Usuario.objects.filter(login=request.session['id']).get()
    #Quantidade de solicitações de amizade
    slct = Solicitacao.objects.filter(amigo=u)
    qtd_solicitacoes = len(slct)
    #Solicitações de desafios
    soli_desafios = Solicitacao_Desafio.objects.filter(usuario_desafiado = u)
    qtd_soli_desafios = len(soli_desafios)
    #Desafios Ativos
    d_ativos_desafiado = Desafio_Ativo.objects.filter(usuario_desafiado = u)
    #Desafios Cumpridos
    d_ativos_desafiante = Desafio_Ativo.objects.filter(usuario_desafiante = u, cumprido = True)
    qtd_d_cumpridos = len(d_ativos_desafiante)
    #Quantidade de Mensagens
    msgs = Mensagens.objects.filter(usuario = u)
    qtd_msgs = len(msgs)
    #{"desafios_cumpridos": qtd_d_cumpridos,"soli_desafios":qtd_soli_desafios, "d_ativos_desafiado":d_ativos_desafiado,"Usuario":u, "qtd_solicitacoes": qtd_solicitacoes}
    #----------------------------------------------------------------------------------------------
    
    qtd_d_ativos_desafiado = len(d_ativos_desafiado)
    ranking_geral = Usuario.objects.all().order_by('-pontos')
    lista_geral = list(ranking_geral)
    pos_geral = lista_geral.index(u) + 1
    
    ranking_turma = Usuario.objects.filter(turma = u.turma).order_by('-pontos')
    lista_turma = list(ranking_turma)
    pos_turma = lista_turma.index(u) + 1
    #"qtd_d_ativos_desafiado": qtd_d_ativos_desafiado,"pos_turma": pos_turma, "pos_geral": pos_geral,"qtd_msgs": qtd_msgs, "desafios_cumpridos": qtd_d_cumpridos,"soli_desafios":qtd_soli_desafios, "d_ativos_desafiado":d_ativos_desafiado, "qtd_solicitacoes": qtd_solicitacoes
    
    
    pesquisa_amigos = Amigos.objects.filter(dono=u)
    minhas_Solicitacoes = Solicitacao.objects.filter(amigo=u) 
    
    mensagem_erro = " "
    pesquisa = Usuario.objects.filter(nome__contains = busca)
    meus_amigos = [] 
    
    for a in pesquisa_amigos:
            meus_amigos.append(a.amigo)
    
    passar = False
    
    if(todos == 'True' and amigos == 'True'):
        mensagem_erro = "Marque somente uma opção!"
        return render(request, 'en/public/Pesquisa.HTML', {"qtd_msgs": qtd_msgs,"msg_erro": mensagem_erro, "Meus": pesquisa_amigos, "Minhas_Solicitacoes": minhas_Solicitacoes, "desafios_cumpridos": qtd_d_cumpridos,"soli_desafios":qtd_soli_desafios, "d_ativos_desafiado":d_ativos_desafiado,"Usuario":u, "qtd_solicitacoes": qtd_solicitacoes, "qtd_d_ativos_desafiado": qtd_d_ativos_desafiado,"pos_turma": pos_turma, "pos_geral": pos_geral,"qtd_msgs": qtd_msgs, "desafios_cumpridos": qtd_d_cumpridos,"soli_desafios":qtd_soli_desafios, "d_ativos_desafiado":d_ativos_desafiado, "qtd_solicitacoes": qtd_solicitacoes})
    
    elif(todos == 'True' and amigos == 'False'):
        
        return render(request, 'en/public/Pesquisa.HTML', {"meus_amigos": meus_amigos,"Pesquisa_Concluida": pesquisa, "qtd_msgs": qtd_msgs,"msg_erro": mensagem_erro, "Minhas_Solicitacoes": minhas_Solicitacoes, "desafios_cumpridos": qtd_d_cumpridos,"soli_desafios":qtd_soli_desafios, "d_ativos_desafiado":d_ativos_desafiado,"Usuario":u, "qtd_solicitacoes": qtd_solicitacoes, "qtd_d_ativos_desafiado": qtd_d_ativos_desafiado,"pos_turma": pos_turma, "pos_geral": pos_geral,"qtd_msgs": qtd_msgs, "desafios_cumpridos": qtd_d_cumpridos,"soli_desafios":qtd_soli_desafios, "d_ativos_desafiado":d_ativos_desafiado, "qtd_solicitacoes": qtd_solicitacoes})
        #return HttpResponse(lista3)
        
    
    elif(todos == 'False' and amigos == 'True'):
        
        amigo_buscado = Usuario.objects.filter(nome__contains = busca)
        pesquisa = Amigos.objects.filter(dono = u, amigo = amigo_buscado)
        return render(request, 'en/public/Pesquisa_Amigos.HTML', {"qtd_msgs": qtd_msgs,"Pesquisa_Concluida": pesquisa,"msg_erro": mensagem_erro, "Meus": pesquisa_amigos, "Minhas_Solicitacoes": minhas_Solicitacoes, "desafios_cumpridos": qtd_d_cumpridos,"soli_desafios":qtd_soli_desafios, "d_ativos_desafiado":d_ativos_desafiado,"Usuario":u, "qtd_solicitacoes": qtd_solicitacoes, "qtd_d_ativos_desafiado": qtd_d_ativos_desafiado,"pos_turma": pos_turma, "pos_geral": pos_geral,"qtd_msgs": qtd_msgs, "desafios_cumpridos": qtd_d_cumpridos,"soli_desafios":qtd_soli_desafios, "d_ativos_desafiado":d_ativos_desafiado, "qtd_solicitacoes": qtd_solicitacoes})
        
    
    elif(todos == 'False' and amigos == 'False'):
        mensagem_erro = "Escolha ao menos uma opção!"
        return render(request, 'en/public/Pesquisa.HTML', {"qtd_msgs": qtd_msgs,"msg_erro": mensagem_erro, "Meus": pesquisa_amigos, "Minhas_Solicitacoes": minhas_Solicitacoes, "desafios_cumpridos": qtd_d_cumpridos,"soli_desafios":qtd_soli_desafios, "d_ativos_desafiado":d_ativos_desafiado,"Usuario":u, "qtd_solicitacoes": qtd_solicitacoes, "qtd_d_ativos_desafiado": qtd_d_ativos_desafiado,"pos_turma": pos_turma, "pos_geral": pos_geral,"qtd_msgs": qtd_msgs, "desafios_cumpridos": qtd_d_cumpridos,"soli_desafios":qtd_soli_desafios, "d_ativos_desafiado":d_ativos_desafiado, "qtd_solicitacoes": qtd_solicitacoes})
        
    
    if(passar == True):return render(request, 'en/public/Pesquisa.HTML', {"qtd_msgs": qtd_msgs,"Pesquisa_Concluida": pesquisa,"msg_erro": mensagem_erro, "Meus": pesquisa_amigos, "Minhas_Solicitacoes": minhas_Solicitacoes, "desafios_cumpridos": qtd_d_cumpridos,"soli_desafios":qtd_soli_desafios, "d_ativos_desafiado":d_ativos_desafiado,"Usuario":u, "qtd_solicitacoes": qtd_solicitacoes, "qtd_d_ativos_desafiado": qtd_d_ativos_desafiado,"pos_turma": pos_turma, "pos_geral": pos_geral,"qtd_msgs": qtd_msgs, "desafios_cumpridos": qtd_d_cumpridos,"soli_desafios":qtd_soli_desafios, "d_ativos_desafiado":d_ativos_desafiado, "qtd_solicitacoes": qtd_solicitacoes})     


@csrf_exempt
def Fazer_Amizade (request):
    #---------------------------Notificações-----------------------------------------------------
    #Sessão do usuario
    u = Usuario.objects.filter(login=request.session['id']).get()
    #Quantidade de solicitações de amizade
    slct = Solicitacao.objects.filter(amigo=u)
    qtd_solicitacoes = len(slct)
    #Solicitações de desafios
    soli_desafios = Solicitacao_Desafio.objects.filter(usuario_desafiado = u)
    qtd_soli_desafios = len(soli_desafios)
    #Desafios Ativos
    d_ativos_desafiado = Desafio_Ativo.objects.filter(usuario_desafiado = u)
    #Desafios Cumpridos
    d_ativos_desafiante = Desafio_Ativo.objects.filter(usuario_desafiante = u, cumprido = True)
    qtd_d_cumpridos = len(d_ativos_desafiante)
    #Quantidade de Mensagens
    msgs = Mensagens.objects.filter(usuario = u)
    qtd_msgs = len(msgs)
    #{"desafios_cumpridos": qtd_d_cumpridos,"soli_desafios":qtd_soli_desafios, "d_ativos_desafiado":d_ativos_desafiado,"Usuario":u, "qtd_solicitacoes": qtd_solicitacoes}
    #----------------------------------------------------------------------------------------------
     
    id_amigo = request.POST['cFazer_amizade']
    
    amigo_solicitado = Usuario.objects.filter(id=id_amigo).get()
    
    solicitacao_amigo_usuario = Solicitacao(usuario=amigo_solicitado, amigo=u, resposta=False)
    solicitacao_usuario_amigo = Solicitacao(usuario=u, amigo=amigo_solicitado, resposta=False)
    mensagem_erro = " "
    
    try:
        verificar_solicitacao_usuario_amigo = Solicitacao.objects.filter(usuario = u, amigo = amigo_solicitado).get()
        
        if(verificar_solicitacao_usuario_amigo != solicitacao_usuario_amigo):
            mensagem_erro = "Já existe uma solicitação!"
            #return HttpResponse(mensagem_erro)
            return render(request, 'en/public/Pesquisa.HTML' ,{"qtd_msgs": qtd_msgs,"msg_erro": mensagem_erro, "desafios_cumpridos": qtd_d_cumpridos,"soli_desafios":qtd_soli_desafios, "d_ativos_desafiado":d_ativos_desafiado,"Usuario":u, "qtd_solicitacoes": qtd_solicitacoes})
        else:
            solicitacao_usuario_amigo.save()
            mensagem_erro = "Solicitação Concluida!"
            #return HttpResponse(mensagem_erro)
            return render(request, 'en/public/Pesquisa.HTML' ,{"qtd_msgs": qtd_msgs,"msg_erro": mensagem_erro, "desafios_cumpridos": qtd_d_cumpridos,"soli_desafios":qtd_soli_desafios, "d_ativos_desafiado":d_ativos_desafiado,"Usuario":u, "qtd_solicitacoes": qtd_solicitacoes })
        
    except:
        
        try:        
    
            verificar_solicitacao_amigo_usuario = Solicitacao.objects.filter(usuario = amigo_solicitado, amigo = u).get()
        
            if(verificar_solicitacao_amigo_usuario != solicitacao_amigo_usuario):
                mensagem_erro = "Já existe uma solicitação!"
                #return HttpResponse(mensagem_erro)
                return render(request, 'en/public/Pesquisa.HTML' ,{"qtd_msgs": qtd_msgs,"msg_erro": mensagem_erro, "desafios_cumpridos": qtd_d_cumpridos,"soli_desafios":qtd_soli_desafios, "d_ativos_desafiado":d_ativos_desafiado,"Usuario":u, "qtd_solicitacoes": qtd_solicitacoes})
        
            else:
                solicitacao_usuario_amigo.save()
                mensagem_erro = "Solicitação Concluida!"
                #return HttpResponse(mensagem_erro)
                return render(request, 'en/public/Pesquisa.HTML' ,{"qtd_msgs": qtd_msgs,"msg_erro": mensagem_erro, "desafios_cumpridos": qtd_d_cumpridos,"soli_desafios":qtd_soli_desafios, "d_ativos_desafiado":d_ativos_desafiado,"Usuario":u, "qtd_solicitacoes": qtd_solicitacoes})
            
        except:
            
            try:
                verificar_amigo = Amigos.objects.filter(dono = u, amigo = amigo_solicitado).get()
                mensagem_erro = "Vocês já são amigos!"
                #return HttpResponse(mensagem_erro)
                return render(request, 'en/public/Pesquisa.HTML' ,{"qtd_msgs": qtd_msgs,"msg_erro": mensagem_erro, "desafios_cumpridos": qtd_d_cumpridos,"soli_desafios":qtd_soli_desafios, "d_ativos_desafiado":d_ativos_desafiado,"Usuario":u, "qtd_solicitacoes": qtd_solicitacoes })
                
                                
            except:
                if(u == amigo_solicitado):
                    mensagem_erro = "Vocês já são amigos!"
                    #return HttpResponse(mensagem_erro)
                    return render(request, 'en/public/Pesquisa.HTML' ,{"qtd_msgs": qtd_msgs,"msg_erro": mensagem_erro, "desafios_cumpridos": qtd_d_cumpridos,"soli_desafios":qtd_soli_desafios, "d_ativos_desafiado":d_ativos_desafiado,"Usuario":u, "qtd_solicitacoes": qtd_solicitacoes })
                
                else:
                    solicitacao_usuario_amigo.save()
                    mensagem_erro = "Solicitação Concluida!"
                    #return HttpResponse(mensagem_erro)
                    return render(request, 'en/public/Pesquisa.HTML' ,{"qtd_msgs": qtd_msgs,"msg_erro": mensagem_erro, "desafios_cumpridos": qtd_d_cumpridos,"soli_desafios":qtd_soli_desafios, "d_ativos_desafiado":d_ativos_desafiado,"Usuario":u, "qtd_solicitacoes": qtd_solicitacoes})
       
            
@csrf_exempt
def Pedido_Solicitacao (request):
    #---------------------------Notificações-----------------------------------------------------
    #Sessão do usuario
    u = Usuario.objects.filter(login=request.session['id']).get()
    #Quantidade de solicitações de amizade
    slct = Solicitacao.objects.filter(amigo=u)
    qtd_solicitacoes = len(slct)
    #Solicitações de desafios
    soli_desafios = Solicitacao_Desafio.objects.filter(usuario_desafiado = u)
    qtd_soli_desafios = len(soli_desafios)
    #Desafios Ativos
    d_ativos_desafiado = Desafio_Ativo.objects.filter(usuario_desafiado = u)
    #Desafios Cumpridos
    d_ativos_desafiante = Desafio_Ativo.objects.filter(usuario_desafiante = u, cumprido = True)
    qtd_d_cumpridos = len(d_ativos_desafiante)
    #Quantidade de Mensagens
    msgs = Mensagens.objects.filter(usuario = u)
    qtd_msgs = len(msgs)
    #{"desafios_cumpridos": qtd_d_cumpridos,"soli_desafios":qtd_soli_desafios, "d_ativos_desafiado":d_ativos_desafiado,"Usuario":u, "qtd_solicitacoes": qtd_solicitacoes}
    #----------------------------------------------------------------------------------------------
    
    pedido = request.POST['cPedido_solicitacao']
    id_usuario = request.POST['cPedido_usuario_id']
    id_pedido = request.POST['cPedido_solicitacao_id']
    
    meusAmigos = Amigos.objects.filter(dono=u)
    minhas_Solicitacoes = Solicitacao.objects.filter(amigo=u)
    
    amigo_pesquisado = Usuario.objects.filter(id=id_usuario).get()
    
    if(pedido == 'True'):
        amigo_remetente = Amigos(dono=u, amigo=amigo_pesquisado)
        amigo_destinatario = Amigos(dono=amigo_pesquisado, amigo=u)

        amigo_remetente.save()
        amigo_destinatario.save()           
        
        solicitacao_atual = Solicitacao.objects.filter(id=id_pedido).get()
        solicitacao_atual.delete()
        
        mensagem_erro = "Amigo Aceito!"
        return render(request, 'en/public/Tela_Amigos.HTML' , {"qtd_msgs": qtd_msgs,"Meus": meusAmigos, "Minhas_Solicitacoes": minhas_Solicitacoes, "desafios_cumpridos": qtd_d_cumpridos,"soli_desafios":qtd_soli_desafios, "d_ativos_desafiado":d_ativos_desafiado,"Usuario":u, "qtd_solicitacoes": qtd_solicitacoes})    
    
    elif(pedido == 'False'):         
        
        solicitacao_atual = Solicitacao.objects.filter(id=id_pedido).get()
        solicitacao_atual.delete()
        
        mensagem_erro = "Convite Recusado!"
        return render(request, 'en/public/Tela_Amigos.HTML' ,{"qtd_msgs": qtd_msgs,"Meus": meusAmigos, "Minhas_Solicitacoes": minhas_Solicitacoes, "desafios_cumpridos": qtd_d_cumpridos,"soli_desafios":qtd_soli_desafios, "d_ativos_desafiado":d_ativos_desafiado,"Usuario":u, "qtd_solicitacoes": qtd_solicitacoes})

def Desafiar (request):
    
    #---------------------------Notificações-----------------------------------------------------
    #Sessão do usuario
    u = Usuario.objects.filter(login=request.session['id']).get()
   
    #Quantidade de solicitações de amizade
    slct = Solicitacao.objects.filter(amigo=u)
    qtd_solicitacoes = len(slct)
    #Solicitações de desafios
    soli_desafios = Solicitacao_Desafio.objects.filter(usuario_desafiado = u)
    qtd_soli_desafios = len(soli_desafios)
    #Desafios Ativos
    d_ativos_desafiado = Desafio_Ativo.objects.filter(usuario_desafiado = u)
    qtd_d_ativos_desafiados = len(d_ativos_desafiado)
    #Desafios Cumpridos
    d_ativos_desafiante = Desafio_Ativo.objects.filter(usuario_desafiante = u, cumprido = True)
    qtd_d_cumpridos = len(d_ativos_desafiante)
    #Quantidade de Mensagens
    msgs = Mensagens.objects.filter(usuario = u)
    qtd_msgs = len(msgs)
    #{"desafios_cumpridos": qtd_d_cumpridos,"soli_desafios":qtd_soli_desafios, "d_ativos_desafiado":d_ativos_desafiado,"Usuario":u, "qtd_solicitacoes": qtd_solicitacoes}
    #----------------------------------------------------------------------------------------------
    
    qtd_d_ativos_desafiado = len(d_ativos_desafiado)
    ranking_geral = Usuario.objects.all().order_by('-pontos')
    lista_geral = list(ranking_geral)
    pos_geral = lista_geral.index(u) + 1
    
    ranking_turma = Usuario.objects.filter(turma = u.turma).order_by('-pontos')
    lista_turma = list(ranking_turma)
    pos_turma = lista_turma.index(u) + 1
    #"qtd_d_ativos_desafiado": qtd_d_ativos_desafiado,"pos_turma": pos_turma, "pos_geral": pos_geral,"qtd_msgs": qtd_msgs, "desafios_cumpridos": qtd_d_cumpridos,"soli_desafios":qtd_soli_desafios, "d_ativos_desafiado":d_ativos_desafiado, "qtd_solicitacoes": qtd_solicitacoes
    
    
    #Busca de desafios e de Amigos
    desafios = Desafio.objects.all() 
    meusAmigos = Amigos.objects.filter(dono = u)
    
    #Consulta para mostrar as solicitações
    soli_desafios = Solicitacao_Desafio.objects.filter(usuario_desafiado = u)
    #Notificação da quantidade de solicitação de desafios
    qtd_soli_desafios = len(soli_desafios)
    
    #Consulta para mostrar os desafios ativos
    d_ativos_desafiado = Desafio_Ativo.objects.filter(usuario_desafiado = u, enviado = False)
    
    #Consulta para mostrar os desafios cumpridos
    d_ativos_desafiante = Desafio_Ativo.objects.filter(usuario_desafiante = u, cumprido = True)
       
    
    return render(request, 'en/public/Desafiar.HTML', {"qtd_d_ativos_desafiados": qtd_d_ativos_desafiados ,"qtd_msgs":qtd_msgs,"d_ativos_desafiante": d_ativos_desafiante, "d_ativos_desafiado": d_ativos_desafiado, "solicit_desafios": soli_desafios, "soli_desafios": qtd_soli_desafios, "desafios": desafios, "meus_amigos": meusAmigos, "desafios_cumpridos": qtd_d_cumpridos,"soli_desafios":qtd_soli_desafios, "d_ativos_desafiado":d_ativos_desafiado,"Usuario":u, "qtd_solicitacoes": qtd_solicitacoes, "qtd_d_ativos_desafiado": qtd_d_ativos_desafiado,"pos_turma": pos_turma, "pos_geral": pos_geral,"qtd_msgs": qtd_msgs, "desafios_cumpridos": qtd_d_cumpridos,"soli_desafios":qtd_soli_desafios, "d_ativos_desafiado":d_ativos_desafiado, "qtd_solicitacoes": qtd_solicitacoes})

def Ativos (request):
    
    #---------------------------Notificações-----------------------------------------------------
    #Sessão do usuario
    u = Usuario.objects.filter(login=request.session['id']).get()
   
    #Quantidade de solicitações de amizade
    slct = Solicitacao.objects.filter(amigo=u)
    qtd_solicitacoes = len(slct)
    #Solicitações de desafios
    soli_desafios = Solicitacao_Desafio.objects.filter(usuario_desafiado = u)
    qtd_soli_desafios = len(soli_desafios)
    #Desafios Ativos
    d_ativos_desafiado = Desafio_Ativo.objects.filter(usuario_desafiado = u)
    qtd_d_ativos_desafiados = len(d_ativos_desafiado)
    #Desafios Cumpridos
    d_ativos_desafiante = Desafio_Ativo.objects.filter(usuario_desafiante = u, cumprido = True)
    qtd_d_cumpridos = len(d_ativos_desafiante)
    #Quantidade de Mensagens
    msgs = Mensagens.objects.filter(usuario = u)
    qtd_msgs = len(msgs)
    #{"desafios_cumpridos": qtd_d_cumpridos,"soli_desafios":qtd_soli_desafios, "d_ativos_desafiado":d_ativos_desafiado,"Usuario":u, "qtd_solicitacoes": qtd_solicitacoes}
    #----------------------------------------------------------------------------------------------
   
    qtd_d_ativos_desafiado = len(d_ativos_desafiado)
    ranking_geral = Usuario.objects.all().order_by('-pontos')
    lista_geral = list(ranking_geral)
    pos_geral = lista_geral.index(u) + 1
    
    ranking_turma = Usuario.objects.filter(turma = u.turma).order_by('-pontos')
    lista_turma = list(ranking_turma)
    pos_turma = lista_turma.index(u) + 1
    #"qtd_d_ativos_desafiado": qtd_d_ativos_desafiado,"pos_turma": pos_turma, "pos_geral": pos_geral,"qtd_msgs": qtd_msgs, "desafios_cumpridos": qtd_d_cumpridos,"soli_desafios":qtd_soli_desafios, "d_ativos_desafiado":d_ativos_desafiado, "qtd_solicitacoes": qtd_solicitacoes
    
    #Busca de desafios e de Amigos
    desafios = Desafio.objects.all() 
    meusAmigos = Amigos.objects.filter(dono = u)
    
    #Consulta para mostrar as solicitações
    soli_desafios = Solicitacao_Desafio.objects.filter(usuario_desafiado = u)
    #Notificação da quantidade de solicitação de desafios
    qtd_soli_desafios = len(soli_desafios)
    
    #Consulta para mostrar os desafios ativos
    d_ativos_desafiado = Desafio_Ativo.objects.filter(usuario_desafiado = u, enviado = False)
    
    #Consulta para mostrar os desafios cumpridos
    d_ativos_desafiante = Desafio_Ativo.objects.filter(usuario_desafiante = u, cumprido = True)
       
    
    return render(request, 'en/public/Ativos.HTML', {"qtd_d_ativos_desafiados": qtd_d_ativos_desafiados ,"qtd_msgs":qtd_msgs,"d_ativos_desafiante": d_ativos_desafiante, "d_ativos_desafiado": d_ativos_desafiado, "solicit_desafios": soli_desafios, "soli_desafios": qtd_soli_desafios, "desafios": desafios, "meus_amigos": meusAmigos, "desafios_cumpridos": qtd_d_cumpridos,"soli_desafios":qtd_soli_desafios, "d_ativos_desafiado":d_ativos_desafiado,"Usuario":u, "qtd_solicitacoes": qtd_solicitacoes, "qtd_d_ativos_desafiado": qtd_d_ativos_desafiado,"pos_turma": pos_turma, "pos_geral": pos_geral,"qtd_msgs": qtd_msgs, "desafios_cumpridos": qtd_d_cumpridos,"soli_desafios":qtd_soli_desafios, "d_ativos_desafiado":d_ativos_desafiado, "qtd_solicitacoes": qtd_solicitacoes})

def Pendentes (request):
    
    #---------------------------Notificações-----------------------------------------------------
    #Sessão do usuario
    u = Usuario.objects.filter(login=request.session['id']).get()
   
    #Quantidade de solicitações de amizade
    slct = Solicitacao.objects.filter(amigo=u)
    qtd_solicitacoes = len(slct)
    #Solicitações de desafios
    soli_desafios = Solicitacao_Desafio.objects.filter(usuario_desafiado = u)
    qtd_soli_desafios = len(soli_desafios)
    #Desafios Ativos
    d_ativos_desafiado = Desafio_Ativo.objects.filter(usuario_desafiado = u)
    qtd_d_ativos_desafiados = len(d_ativos_desafiado)
    #Desafios Cumpridos
    d_ativos_desafiante = Desafio_Ativo.objects.filter(usuario_desafiante = u, cumprido = True)
    qtd_d_cumpridos = len(d_ativos_desafiante)
    #Quantidade de Mensagens
    msgs = Mensagens.objects.filter(usuario = u)
    qtd_msgs = len(msgs)
    #{"desafios_cumpridos": qtd_d_cumpridos,"soli_desafios":qtd_soli_desafios, "d_ativos_desafiado":d_ativos_desafiado,"Usuario":u, "qtd_solicitacoes": qtd_solicitacoes}
    #----------------------------------------------------------------------------------------------
   
    qtd_d_ativos_desafiado = len(d_ativos_desafiado)
    ranking_geral = Usuario.objects.all().order_by('-pontos')
    lista_geral = list(ranking_geral)
    pos_geral = lista_geral.index(u) + 1
    
    ranking_turma = Usuario.objects.filter(turma = u.turma).order_by('-pontos')
    lista_turma = list(ranking_turma)
    pos_turma = lista_turma.index(u) + 1
    #"qtd_d_ativos_desafiado": qtd_d_ativos_desafiado,"pos_turma": pos_turma, "pos_geral": pos_geral,"qtd_msgs": qtd_msgs, "desafios_cumpridos": qtd_d_cumpridos,"soli_desafios":qtd_soli_desafios, "d_ativos_desafiado":d_ativos_desafiado, "qtd_solicitacoes": qtd_solicitacoes
    
    #Busca de desafios e de Amigos
    desafios = Desafio.objects.all() 
    meusAmigos = Amigos.objects.filter(dono = u)
    
    #Consulta para mostrar as solicitações
    soli_desafios = Solicitacao_Desafio.objects.filter(usuario_desafiado = u)
    #Notificação da quantidade de solicitação de desafios
    qtd_soli_desafios = len(soli_desafios)
    
    #Consulta para mostrar os desafios ativos
    d_ativos_desafiado = Desafio_Ativo.objects.filter(usuario_desafiado = u, enviado = False)
    
    #Consulta para mostrar os desafios cumpridos
    d_ativos_desafiante = Desafio_Ativo.objects.filter(usuario_desafiante = u, cumprido = True)
       
    
    return render(request, 'en/public/Pendentes.HTML', {"qtd_d_ativos_desafiados": qtd_d_ativos_desafiados ,"qtd_msgs":qtd_msgs,"d_ativos_desafiante": d_ativos_desafiante, "d_ativos_desafiado": d_ativos_desafiado, "solicit_desafios": soli_desafios, "soli_desafios": qtd_soli_desafios, "desafios": desafios, "meus_amigos": meusAmigos, "desafios_cumpridos": qtd_d_cumpridos,"soli_desafios":qtd_soli_desafios, "d_ativos_desafiado":d_ativos_desafiado,"Usuario":u, "qtd_solicitacoes": qtd_solicitacoes, "qtd_d_ativos_desafiado": qtd_d_ativos_desafiado,"pos_turma": pos_turma, "pos_geral": pos_geral,"qtd_msgs": qtd_msgs, "desafios_cumpridos": qtd_d_cumpridos,"soli_desafios":qtd_soli_desafios, "d_ativos_desafiado":d_ativos_desafiado, "qtd_solicitacoes": qtd_solicitacoes})


def Cumpridos (request):
    
    #---------------------------Notificações-----------------------------------------------------
    #Sessão do usuario
    u = Usuario.objects.filter(login=request.session['id']).get()
   
    #Quantidade de solicitações de amizade
    slct = Solicitacao.objects.filter(amigo=u)
    qtd_solicitacoes = len(slct)
    #Solicitações de desafios
    soli_desafios = Solicitacao_Desafio.objects.filter(usuario_desafiado = u)
    qtd_soli_desafios = len(soli_desafios)
    #Desafios Ativos
    d_ativos_desafiado = Desafio_Ativo.objects.filter(usuario_desafiado = u)
    qtd_d_ativos_desafiados = len(d_ativos_desafiado)
    #Desafios Cumpridos
    d_ativos_desafiante = Desafio_Ativo.objects.filter(usuario_desafiante = u, cumprido = True)
    qtd_d_cumpridos = len(d_ativos_desafiante)
    #Quantidade de Mensagens
    msgs = Mensagens.objects.filter(usuario = u)
    qtd_msgs = len(msgs)
    #{"desafios_cumpridos": qtd_d_cumpridos,"soli_desafios":qtd_soli_desafios, "d_ativos_desafiado":d_ativos_desafiado,"Usuario":u, "qtd_solicitacoes": qtd_solicitacoes}
    #----------------------------------------------------------------------------------------------
   
    qtd_d_ativos_desafiado = len(d_ativos_desafiado)
    ranking_geral = Usuario.objects.all().order_by('-pontos')
    lista_geral = list(ranking_geral)
    pos_geral = lista_geral.index(u) + 1
    
    ranking_turma = Usuario.objects.filter(turma = u.turma).order_by('-pontos')
    lista_turma = list(ranking_turma)
    pos_turma = lista_turma.index(u) + 1
    #"qtd_d_ativos_desafiado": qtd_d_ativos_desafiado,"pos_turma": pos_turma, "pos_geral": pos_geral,"qtd_msgs": qtd_msgs, "desafios_cumpridos": qtd_d_cumpridos,"soli_desafios":qtd_soli_desafios, "d_ativos_desafiado":d_ativos_desafiado, "qtd_solicitacoes": qtd_solicitacoes
    
    #Busca de desafios e de Amigos
    desafios = Desafio.objects.all() 
    meusAmigos = Amigos.objects.filter(dono = u)
    
    #Consulta para mostrar as solicitações
    soli_desafios = Solicitacao_Desafio.objects.filter(usuario_desafiado = u)
    #Notificação da quantidade de solicitação de desafios
    qtd_soli_desafios = len(soli_desafios)
    
    #Consulta para mostrar os desafios ativos
    d_ativos_desafiado = Desafio_Ativo.objects.filter(usuario_desafiado = u, enviado = False)
    
    #Consulta para mostrar os desafios cumpridos
    d_ativos_desafiante = Desafio_Ativo.objects.filter(usuario_desafiante = u, cumprido = True)
       
    
    return render(request, 'en/public/Cumpridos.HTML', {"qtd_d_ativos_desafiados": qtd_d_ativos_desafiados ,"qtd_msgs":qtd_msgs,"d_ativos_desafiante": d_ativos_desafiante, "d_ativos_desafiado": d_ativos_desafiado, "solicit_desafios": soli_desafios, "soli_desafios": qtd_soli_desafios, "desafios": desafios, "meus_amigos": meusAmigos, "desafios_cumpridos": qtd_d_cumpridos,"soli_desafios":qtd_soli_desafios, "d_ativos_desafiado":d_ativos_desafiado,"Usuario":u, "qtd_solicitacoes": qtd_solicitacoes, "qtd_d_ativos_desafiado": qtd_d_ativos_desafiado,"pos_turma": pos_turma, "pos_geral": pos_geral,"qtd_msgs": qtd_msgs, "desafios_cumpridos": qtd_d_cumpridos,"soli_desafios":qtd_soli_desafios, "d_ativos_desafiado":d_ativos_desafiado, "qtd_solicitacoes": qtd_solicitacoes})


@csrf_exempt
def Lancar_Desafios(request):
    
    #---------------------------Notificações-----------------------------------------------------
    #Sessão do usuario
    u = Usuario.objects.filter(login=request.session['id']).get()
    #Quantidade de solicitações de amizade
    slct = Solicitacao.objects.filter(amigo=u)
    qtd_solicitacoes = len(slct)
    #Solicitações de desafios
    soli_desafios = Solicitacao_Desafio.objects.filter(usuario_desafiado = u)
    qtd_soli_desafios = len(soli_desafios)
    #Desafios Ativos
    d_ativos_desafiado = Desafio_Ativo.objects.filter(usuario_desafiado = u)
    #Desafios Cumpridos
    d_ativos_desafiante = Desafio_Ativo.objects.filter(usuario_desafiante = u, cumprido = True)
    qtd_d_cumpridos = len(d_ativos_desafiante)
    #Quantidade de Mensagens
    msgs = Mensagens.objects.filter(usuario = u)
    qtd_msgs = len(msgs)
    #{"desafios_cumpridos": qtd_d_cumpridos,"soli_desafios":qtd_soli_desafios, "d_ativos_desafiado":d_ativos_desafiado,"Usuario":u, "qtd_solicitacoes": qtd_solicitacoes}
    #----------------------------------------------------------------------------------------------
    
    desafio = request.POST.get("cDesafios", False)
    amigo = request.POST.get("cAmigos", False)
    
    
    #consulta de desafios e amigos
    amigo_desafiado = Usuario.objects.filter(id = amigo).get()
    desafio_solicitado = Desafio.objects.filter(id = desafio).get()
    
    #Mostrar desafios e amigos apos enviar
    desafios = Desafio.objects.all() 
    meusAmigos = Amigos.objects.filter(dono = u)
    
    #Consulta para mostrar as solicitações
    soli_desafios = Solicitacao_Desafio.objects.filter(usuario_desafiado = u)
    #Notificação da quantidade de solicitação de desafios
    qtd_soli_desafios = len(soli_desafios)
    
    #Consulta para mostrar os desafios ativos
    d_ativos_desafiado = Desafio_Ativo.objects.filter(usuario_desafiado = u)
    qtd_desafios_ativos = len(d_ativos_desafiado)
    
    #Consulta para mostrar os desafios cumpridos
    d_ativos_desafiante = Desafio_Ativo.objects.filter(usuario_desafiante = u, cumprido = True)
    qtd_desafios_amigo = len(d_ativos_desafiado)
    
    if(qtd_desafios_ativos <= 10 and qtd_desafios_amigo <= 10):
    
        #criando uma solicitação
        try:
            
            consulta_solicitacao_desafio = Solicitacao_Desafio.objects.filter(usuario_desafiante = u, usuario_desafiado = amigo_desafiado, desafio = desafio_solicitado, resposta = False).get()      
            mensagem = "Esse desafio já foi enviado!"
            return render(request, 'en/public/Tela_Desafios.HTML', {"qtd_msgs":qtd_msgs,"d_ativos_desafiante": d_ativos_desafiante, "d_ativos_desafiado": d_ativos_desafiado, "solicit_desafios": soli_desafios, "msg_erro": mensagem, "desafios": desafios, "meus_amigos": meusAmigos, "desafios_cumpridos": qtd_d_cumpridos,"soli_desafios":qtd_soli_desafios, "d_ativos_desafiado":d_ativos_desafiado,"Usuario":u, "qtd_solicitacoes": qtd_solicitacoes})
        
        except:
            
            try:
                
                consulta_solicitacao_desafio = Solicitacao_Desafio.objects.filter(usuario_desafiante = amigo_desafiado, usuario_desafiado = u, desafio = desafio_solicitado, resposta = False).get()      
                mensagem = "Esse desafio já foi enviado!"
                return render(request, 'en/public/Tela_Desafios.HTML', {"qtd_msgs":qtd_msgs,"d_ativos_desafiante": d_ativos_desafiante, "d_ativos_desafiado": d_ativos_desafiado, "solicit_desafios": soli_desafios, "msg_erro": mensagem, "desafios": desafios, "meus_amigos": meusAmigos, "desafios_cumpridos": qtd_d_cumpridos,"soli_desafios":qtd_soli_desafios, "d_ativos_desafiado":d_ativos_desafiado,"Usuario":u, "qtd_solicitacoes": qtd_solicitacoes })
            
            except:
                
                criar_soli_desafio = Solicitacao_Desafio(usuario_desafiante = u, usuario_desafiado = amigo_desafiado, desafio = desafio_solicitado, resposta = False)
                criar_soli_desafio.save()
                
                #mensagem de erro
                mensagem = "Desafio Enviado!"
            
                return render(request, 'en/public/Tela_Desafios.HTML', {"qtd_msgs":qtd_msgs,"d_ativos_desafiante": d_ativos_desafiante, "d_ativos_desafiado": d_ativos_desafiado, "solicit_desafios": soli_desafios, "msg_erro": mensagem, "desafios": desafios, "meus_amigos": meusAmigos, "desafios_cumpridos": qtd_d_cumpridos,"soli_desafios":qtd_soli_desafios, "d_ativos_desafiado":d_ativos_desafiado,"Usuario":u, "qtd_solicitacoes": qtd_solicitacoes})

    else:
            
        mensagem = "Usuarios com limite de desafios!"
        return render(request, 'en/public/Tela_Desafios.HTML', {"qtd_msgs":qtd_msgs,"d_ativos_desafiante": d_ativos_desafiante, "d_ativos_desafiado": d_ativos_desafiado, "solicit_desafios": soli_desafios, "msg_erro": mensagem, "desafios": desafios, "meus_amigos": meusAmigos, "desafios_cumpridos": qtd_d_cumpridos,"soli_desafios":qtd_soli_desafios, "d_ativos_desafiado":d_ativos_desafiado,"Usuario":u, "qtd_solicitacoes": qtd_solicitacoes })


@csrf_exempt
def Lancar_Desafio_Turma(request):
    
    u = Usuario.objects.filter(login=request.session['id']).get()
     
    desafio = request.POST.get("cDesafios", False)
    turma_escolhida = request.POST.get("cTurma", False)
    
    desafio_escolhido = Desafio.objects.filter(id = desafio).get()
    
    alunos_turma = Usuario.objects.filter(turma = turma_escolhida)
    
    for a in alunos_turma:
        criar_soli_desafio = Solicitacao_Desafio(usuario_desafiante = u, usuario_desafiado = a, desafio = desafio_escolhido, resposta = False)
        criar_soli_desafio.save()
    
    
    return Desafiar(request)
    
    
    
def Pedido_Desafio(request):
    #---------------------------Notificações-----------------------------------------------------
    #Sessão do usuario
    u = Usuario.objects.filter(login=request.session['id']).get()
    #Quantidade de solicitações de amizade
    slct = Solicitacao.objects.filter(amigo=u)
    qtd_solicitacoes = len(slct)
    #Solicitações de desafios
    soli_desafios = Solicitacao_Desafio.objects.filter(usuario_desafiado = u)
    qtd_soli_desafios = len(soli_desafios)
    #Desafios Ativos
    d_ativos_desafiado = Desafio_Ativo.objects.filter(usuario_desafiado = u)
    #Desafios Cumpridos
    d_ativos_desafiante = Desafio_Ativo.objects.filter(usuario_desafiante = u, cumprido = True)
    qtd_d_cumpridos = len(d_ativos_desafiante)
    #Quantidade de Mensagens
    msgs = Mensagens.objects.filter(usuario = u)
    qtd_msgs = len(msgs)
    #{"desafios_cumpridos": qtd_d_cumpridos,"soli_desafios":qtd_soli_desafios, "d_ativos_desafiado":d_ativos_desafiado,"Usuario":u, "qtd_solicitacoes": qtd_solicitacoes}
    #----------------------------------------------------------------------------------------------
    
    pedido_desafio = request.POST["cPedido_solicitacao"]
    u_desafiante = request.POST["cPedido_usuario_id"]
    desafio_p = request.POST["cPedido_desafio_id"]
    soli = request.POST["cPedido_id"]
    
    
    Usuario_desafiante = Usuario.objects.filter(id = u_desafiante).get()
    desafio_proposto = Desafio.objects.filter(id = desafio_p).get()
    soli_desafio = Solicitacao_Desafio.objects.filter(id = soli).get()
    
    #Mostrar desafios e amigos apos enviar
    desafios = Desafio.objects.all() 
    meusAmigos = Amigos.objects.filter(dono = u)
    
    #Consulta para mostrar as solicitações
    soli_desafios = Solicitacao_Desafio.objects.filter(usuario_desafiado = u)
        
    #Consulta para mostrar os desafios ativos
    d_ativos_desafiado = Desafio_Ativo.objects.filter(usuario_desafiado = u)
    qtd_d_ativos = len(d_ativos_desafiado)
    
    #Consulta para mostrar os desafios cumpridos
    d_ativos_desafiante = Desafio_Ativo.objects.filter(usuario_desafiante = u, cumprido = True) 
         
    if(pedido_desafio == 'True'):
        
        if(qtd_d_ativos <= 10):
        
            desafio_ativo_desafiado = Desafio_Ativo(usuario_desafiante = Usuario_desafiante, usuario_desafiado = u, postagem = None, desafio = desafio_proposto, cumprido = False, enviado = False)
            desafio_ativo_desafiado.save()
            
            desafio_ativo_desafiante = Desafio_Ativo(usuario_desafiante = u, usuario_desafiado = Usuario_desafiante, postagem = None, desafio = desafio_proposto, cumprido = False, enviado = False)
            desafio_ativo_desafiante.save()
            
            soli_desafio.delete()
            
            mensagem = "Desafio aceito!"   
            
            #Consulta para mostrar os desafios ativos
            d_ativos_desafiado = Desafio_Ativo.objects.filter(usuario_desafiado = u)
            qtd_d_ativos = len(d_ativos_desafiado)
    
            
            return render(request, 'en/public/Tela_Desafios.HTML', {"qtd_msgs":qtd_msgs,"d_ativos_desafiante": d_ativos_desafiante, "d_ativos_desafiado": d_ativos_desafiado,  "msg_erro": mensagem, "desafios": desafios, "meus_amigos": meusAmigos, "desafios_cumpridos": qtd_d_cumpridos,"soli_desafios":qtd_soli_desafios, "d_ativos_desafiado":d_ativos_desafiado,"Usuario":u, "qtd_solicitacoes": qtd_solicitacoes})
        
        else:
            
            mensagem = "Você já possui o limite de desafios!"   
            
            return render(request, 'en/public/Tela_Desafios.HTML', {"qtd_msgs":qtd_msgs,"d_ativos_desafiante": d_ativos_desafiante, "d_ativos_desafiado": d_ativos_desafiado,  "msg_erro": mensagem, "desafios": desafios, "meus_amigos": meusAmigos, "desafios_cumpridos": qtd_d_cumpridos,"soli_desafios":qtd_soli_desafios, "d_ativos_desafiado":d_ativos_desafiado,"Usuario":u, "qtd_solicitacoes": qtd_solicitacoes})
    elif(pedido_desafio == 'False'):
        soli_desafio.delete()
        
        mensagem = "Desafio Recusado!"   
        
        return render(request, 'en/public/Tela_Desafios.HTML', {"qtd_msgs":qtd_msgs,"d_ativos_desafiante": d_ativos_desafiante, "d_ativos_desafiado": d_ativos_desafiado,  "msg_erro": mensagem, "desafios": desafios, "meus_amigos": meusAmigos, "desafios_cumpridos": qtd_d_cumpridos,"soli_desafios":qtd_soli_desafios, "d_ativos_desafiado":d_ativos_desafiado,"Usuario":u, "qtd_solicitacoes": qtd_solicitacoes})
 
    
    
@csrf_exempt    
def Cumprir_Desafio (request):
    #---------------------------Notificações-----------------------------------------------------
    #Sessão do usuario
    u = Usuario.objects.filter(login=request.session['id']).get()
    #Quantidade de solicitações de amizade
    slct = Solicitacao.objects.filter(amigo=u)
    qtd_solicitacoes = len(slct)
    #Solicitações de desafios
    soli_desafios = Solicitacao_Desafio.objects.filter(usuario_desafiado = u)
    qtd_soli_desafios = len(soli_desafios)
    #Desafios Ativos
    d_ativos_desafiado = Desafio_Ativo.objects.filter(usuario_desafiado = u)
    #Desafios Cumpridos
    d_ativos_desafiante = Desafio_Ativo.objects.filter(usuario_desafiante = u, cumprido = True)
    qtd_d_cumpridos = len(d_ativos_desafiante)
    #Quantidade de Mensagens
    msgs = Mensagens.objects.filter(usuario = u)
    qtd_msgs = len(msgs)
    #{"desafios_cumpridos": qtd_d_cumpridos,"soli_desafios":qtd_soli_desafios, "d_ativos_desafiado":d_ativos_desafiado,"Usuario":u, "qtd_solicitacoes": qtd_solicitacoes}
    #----------------------------------------------------------------------------------------------
    
    id_desafio_ativo = request.POST["id_desafio_ativo"]
    
    desafio_ativo = Desafio_Ativo.objects.filter(id = id_desafio_ativo).get()
    
    return render(request, 'en/public/Cumprir_Desafio.HTML', {"qtd_msgs":qtd_msgs,"desafio_atual": desafio_ativo, "desafios_cumpridos": qtd_d_cumpridos,"soli_desafios":qtd_soli_desafios, "d_ativos_desafiado":d_ativos_desafiado,"Usuario":u, "qtd_solicitacoes": qtd_solicitacoes})
        
    
def Postar_Desafio (request):
    #---------------------------Notificações-----------------------------------------------------
    #Sessão do usuario
    u = Usuario.objects.filter(login=request.session['id']).get()
    #Quantidade de solicitações de amizade
    slct = Solicitacao.objects.filter(amigo=u)
    qtd_solicitacoes = len(slct)
    #Solicitações de desafios
    soli_desafios = Solicitacao_Desafio.objects.filter(usuario_desafiado = u)
    qtd_soli_desafios = len(soli_desafios)
    #Desafios Ativos
    d_ativos_desafiado = Desafio_Ativo.objects.filter(usuario_desafiado = u)
    #Desafios Cumpridos
    d_ativos_desafiante = Desafio_Ativo.objects.filter(usuario_desafiante = u, cumprido = True)
    qtd_d_cumpridos = len(d_ativos_desafiante)
    #Quantidade de Mensagens
    msgs = Mensagens.objects.filter(usuario = u)
    qtd_msgs = len(msgs)
    #{"desafios_cumpridos": qtd_d_cumpridos,"soli_desafios":qtd_soli_desafios, "d_ativos_desafiado":d_ativos_desafiado,"Usuario":u, "qtd_solicitacoes": qtd_solicitacoes}
    #----------------------------------------------------------------------------------------------
    
    Texto = request.POST.get('mensagem', False)
    Foto = request.FILES.get('arquivo', False)
    desafio_ativo = request.POST["cDesafio_Ativo"]
    
    qtd_post = TimeLine.objects.all()
    add_post = len(qtd_post) + 1
    
    hora_atual = datetime.now() 
    competicao_atual = Competicao.objects.filter(ativo = True).get()
    
    passar = False  
     
    if(Texto != False and Foto != False):
        
        time = Beta_TimeLine(id = add_post, text=Texto, competicao = competicao_atual, usuario=u, foto=Foto, date = hora_atual)
        time.save()
        
        cont_post = Cont_Postagem.objects.filter(id = 1).get()
        cont_post.qtd = add_post
        cont_post.save()
                    
        passar=True
        
    
    elif(Texto != False):        
        
        time = Beta_TimeLine(id = add_post, text=Texto, usuario=u, competicao = competicao_atual, foto=Foto, date = hora_atual)
        time.save()
        
        cont_post = Cont_Postagem.objects.filter(id = 1).get()
        cont_post.qtd = add_post
        cont_post.save()
        
        passar=True
        
    else:
            
        passar=True
       
    if(passar): return render(request, 'en/public/Ver_Postagem_Desafio.HTML', {"qtd_msgs":qtd_msgs,"id_desafio": desafio_ativo, "entries": time, "desafios_cumpridos": qtd_d_cumpridos,"soli_desafios":qtd_soli_desafios, "d_ativos_desafiado":d_ativos_desafiado,"Usuario":u, "qtd_solicitacoes": qtd_solicitacoes})
    




@csrf_exempt  
def Lancar_Desafio(request):
    id_postagem = request.POST.get("cId", False)
    id_desafio = request.POST.get("cId_desafio", False)
    
    #Filtrar a postagem beta
    postagem = Beta_TimeLine.objects.filter(id = id_postagem).get()
    #filtrar o desafio ativo
    desafio_ativo = Desafio_Ativo.objects.filter(id = id_desafio).get()
    
    #atribuindo a postagem os campos de desafios
    postagem.desafio = True
    postagem.nome_desafio = desafio_ativo.desafio.nome
    postagem.save()
    
    #criando uma instancia de timeline
    time = TimeLine(id = postagem.id, date = postagem.date, text = postagem.text, competicao = postagem.competicao ,usuario = postagem.usuario, foto = postagem.foto, qtd_coments = postagem.qtd_coments, nome_desafio = postagem.nome_desafio, desafio = postagem.desafio)
    time.save()
    
    #atribuindo a tabela de desafio a postagem
    desafio_ativo.postagem = time
  
    #Atribuindo os campos de cumprido e enviado
    desafio_ativo.cumprido = True
    desafio_ativo.enviado = True
    desafio_ativo.save()
    
    #excluindo a postagem beta
    postagem.delete()
    
    return Timeline(request)

@csrf_exempt     
def Verificar_Desafio (request):
    #---------------------------Notificações-----------------------------------------------------
    #Sessão do usuario
    u = Usuario.objects.filter(login=request.session['id']).get()
    #Quantidade de solicitações de amizade
    slct = Solicitacao.objects.filter(amigo=u)
    qtd_solicitacoes = len(slct)
    #Solicitações de desafios
    soli_desafios = Solicitacao_Desafio.objects.filter(usuario_desafiado = u)
    qtd_soli_desafios = len(soli_desafios)
    #Desafios Ativos
    d_ativos_desafiado = Desafio_Ativo.objects.filter(usuario_desafiado = u)
    #Desafios Cumpridos
    d_ativos_desafiante = Desafio_Ativo.objects.filter(usuario_desafiante = u, cumprido = True)
    qtd_d_cumpridos = len(d_ativos_desafiante)
    #Quantidade de Mensagens
    msgs = Mensagens.objects.filter(usuario = u)
    qtd_msgs = len(msgs)
    #{"desafios_cumpridos": qtd_d_cumpridos,"soli_desafios":qtd_soli_desafios, "d_ativos_desafiado":d_ativos_desafiado,"Usuario":u, "qtd_solicitacoes": qtd_solicitacoes}
    #----------------------------------------------------------------------------------------------
    
    id_desafio = request.POST["id_desafio_ativo"]
    desafio = Desafio_Ativo.objects.filter(id = id_desafio).get()
    
    return render(request, 'en/public/Visualizar_Postagem_Desafio.HTML', {"qtd_msgs":qtd_msgs,"desafio": desafio,"desafios_cumpridos": qtd_d_cumpridos,"soli_desafios":qtd_soli_desafios, "d_ativos_desafiado":d_ativos_desafiado,"Usuario":u, "qtd_solicitacoes": qtd_solicitacoes})

def Atribuir_Desafio (request):
    id_usuario = request.POST.get("cId_usuario", False)
    id_desafio = request.POST.get("cId_desafio_ativo", False)
    opc = request.POST.get("cValor", False)
    
    usu = Usuario.objects.filter(id=id_usuario).get()
    desafio = Desafio_Ativo.objects.filter(id=id_desafio).get()
    dsf = desafio
    
    if(opc == 'True'):
        usu.pontos = usu.pontos + desafio.desafio.pontuacao
        usu.save()
    
        msg = "Você recebeu %s pontos por ter cumprido o desafio %s " % (desafio.desafio.pontuacao, desafio.desafio.nome)
        
        not_msg = Mensagens(usuario = desafio.usuario_desafiado, mensagem = msg)
        not_msg.save()
        
        desafio.delete()
        
        ucs = Usu_Comp_Semanal.objects.filter(usuario = usu).get()
        ucs.qtd_desafios = ucs.qtd_desafios + 1
        ucs.save()
            
        return Atribuir_Conquistas(request, usu, dsf)
            
    elif(opc == 'False'):
        msg = "Você não conseguiu concluir o desafio %s" % (desafio.desafio.nome)
        not_msg = Mensagens(usuario = desafio.usuario_desafiado, mensagem = msg)
        not_msg.save()
        
        desafio.delete()
        return Timeline(request)
    
def Campeoes (request):
    #---------------------------Notificações-----------------------------------------------------
    #Sessão do usuario
    u = Usuario.objects.filter(login=request.session['id']).get()
    #Quantidade de solicitações de amizade
    slct = Solicitacao.objects.filter(amigo=u)
    qtd_solicitacoes = len(slct)
    #Solicitações de desafios
    soli_desafios = Solicitacao_Desafio.objects.filter(usuario_desafiado = u)
    qtd_soli_desafios = len(soli_desafios)
    #Desafios Ativos
    d_ativos_desafiado = Desafio_Ativo.objects.filter(usuario_desafiado = u)
    #Desafios Cumpridos
    d_ativos_desafiante = Desafio_Ativo.objects.filter(usuario_desafiante = u, cumprido = True)
    qtd_d_cumpridos = len(d_ativos_desafiante)
    #Quantidade de Mensagens
    msgs = Mensagens.objects.filter(usuario = u)
    qtd_msgs = len(msgs)
    #{"desafios_cumpridos": qtd_d_cumpridos,"soli_desafios":qtd_soli_desafios, "d_ativos_desafiado":d_ativos_desafiado,"Usuario":u, "qtd_solicitacoes": qtd_solicitacoes}
    #----------------------------------------------------------------------------------------------
    
    qtd_d_ativos_desafiado = len(d_ativos_desafiado)
    ranking_geral = Usuario.objects.all().order_by('-pontos')
    lista_geral = list(ranking_geral)
    pos_geral = lista_geral.index(u) + 1
    
    ranking_turma = Usuario.objects.filter(turma = u.turma).order_by('-pontos')
    lista_turma = list(ranking_turma)
    pos_turma = lista_turma.index(u) + 1
    #"qtd_d_ativos_desafiado": qtd_d_ativos_desafiado,"pos_turma": pos_turma, "pos_geral": pos_geral,"qtd_msgs": qtd_msgs, "desafios_cumpridos": qtd_d_cumpridos,"soli_desafios":qtd_soli_desafios, "d_ativos_desafiado":d_ativos_desafiado, "qtd_solicitacoes": qtd_solicitacoes
    
    #ranking turma
    #ranking = Usuario.objects.filter(turma = u.turma).order_by('-pontos')
    
    #ranking geral
    top1 = Campeao.objects.all().order_by('-mes')

    ranking_geral = Usuario.objects.all().order_by('-pontos')
    
    competicao_atual = Competicao.objects.filter(ativo = True).get()
    

    data_torneio = competicao_atual.data_fim
    
    data_atual = timezone.now()
    
    if(data_atual > data_torneio):
        campeao_geral = Campeao(mes = data_torneio.month, usuario = ranking_geral[0], pontuacao = ranking_geral[0].pontos ,geral = True, turma = False)
        campeao_geral.save()
        
        mes = data_atual.month + 1
        
        if(mes < 12):
            nova_data = data_atual.replace(month = mes, hour=12, minute=0)
        
            nova_comp = Competicao(data_inicio = data_atual, data_fim = nova_data, ativo = True)
            nova_comp.save()
            
            competicao_atual.ativo = False
            competicao_atual.save()
            
            
            u_geral = Usuario.objects.all()
            
            
            for e in u_geral:
                historico = hist_pontuacao(usuario = e, pontuacao = e.pontos , competicao = competicao_atual)
                historico.save()
                
                e.pontos = 0
                e.save()
            
            return render(request, 'en/public/Campeoes.HTML' , {"top1": top1, "qtd_msgs":qtd_msgs, "desafios_cumpridos": qtd_d_cumpridos,"soli_desafios":qtd_soli_desafios, "d_ativos_desafiado":d_ativos_desafiado,"Usuario":u, "qtd_solicitacoes": qtd_solicitacoes, "qtd_d_ativos_desafiado": qtd_d_ativos_desafiado,"pos_turma": pos_turma, "pos_geral": pos_geral,"qtd_msgs": qtd_msgs, "desafios_cumpridos": qtd_d_cumpridos,"soli_desafios":qtd_soli_desafios, "d_ativos_desafiado":d_ativos_desafiado, "qtd_solicitacoes": qtd_solicitacoes})
        
        else:
            ano = data_atual.year + 1
             
            nova_data = data_atual.replace(year = ano, month = 1, hour=12, minute=0)
        
            nova_comp = Competicao(data_inicio = data_atual, data_fim = nova_data, ativo = True)
            nova_comp.save()
            
            competicao_atual.ativo = False
            competicao_atual.save()
        
            
            for e in u_geral:
                e.pontos = 0
                e.save()
        
            return render(request, 'en/public/Campeoes.HTML' , {"top1": top1, "qtd_msgs":qtd_msgs, "desafios_cumpridos": qtd_d_cumpridos,"soli_desafios":qtd_soli_desafios, "d_ativos_desafiado":d_ativos_desafiado,"Usuario":u, "qtd_solicitacoes": qtd_solicitacoes, "qtd_d_ativos_desafiado": qtd_d_ativos_desafiado,"pos_turma": pos_turma, "pos_geral": pos_geral,"qtd_msgs": qtd_msgs, "desafios_cumpridos": qtd_d_cumpridos,"soli_desafios":qtd_soli_desafios, "d_ativos_desafiado":d_ativos_desafiado, "qtd_solicitacoes": qtd_solicitacoes})
        
    else:
        return render(request, 'en/public/Campeoes.HTML' , {"top1": top1, "qtd_msgs":qtd_msgs, "desafios_cumpridos": qtd_d_cumpridos,"soli_desafios":qtd_soli_desafios, "d_ativos_desafiado":d_ativos_desafiado,"Usuario":u, "qtd_solicitacoes": qtd_solicitacoes, "qtd_d_ativos_desafiado": qtd_d_ativos_desafiado,"pos_turma": pos_turma, "pos_geral": pos_geral,"qtd_msgs": qtd_msgs, "desafios_cumpridos": qtd_d_cumpridos,"soli_desafios":qtd_soli_desafios, "d_ativos_desafiado":d_ativos_desafiado, "qtd_solicitacoes": qtd_solicitacoes})

def Conquistas (request):
    u = Usuario.objects.filter(login=request.session['id']).get()
    #Quantidade de solicitações de amizade
    slct = Solicitacao.objects.filter(amigo=u)
    qtd_solicitacoes = len(slct)
    #Solicitações de desafios
    soli_desafios = Solicitacao_Desafio.objects.filter(usuario_desafiado = u)
    qtd_soli_desafios = len(soli_desafios)
    #Desafios Ativos
    d_ativos_desafiado = Desafio_Ativo.objects.filter(usuario_desafiado = u)
    #Desafios Cumpridos
    d_ativos_desafiante = Desafio_Ativo.objects.filter(usuario_desafiante = u, cumprido = True)
    qtd_d_cumpridos = len(d_ativos_desafiante)
    #Quantidade de Mensagens
    msgs = Mensagens.objects.filter(usuario = u)
    qtd_msgs = len(msgs)
    #{"desafios_cumpridos": qtd_d_cumpridos,"soli_desafios":qtd_soli_desafios, "d_ativos_desafiado":d_ativos_desafiado,"Usuario":u, "qtd_solicitacoes": qtd_solicitacoes}
    #----------------------------------------------------------------------------------------------
    qtd_d_ativos_desafiado = len(d_ativos_desafiado)
    ranking_geral = Usuario.objects.all().order_by('-pontos')
    lista_geral = list(ranking_geral)
    pos_geral = lista_geral.index(u) + 1
    
    ranking_turma = Usuario.objects.filter(turma = u.turma).order_by('-pontos')
    lista_turma = list(ranking_turma)
    pos_turma = lista_turma.index(u) + 1
    #"qtd_d_ativos_desafiado": qtd_d_ativos_desafiado,"pos_turma": pos_turma, "pos_geral": pos_geral,"qtd_msgs": qtd_msgs, "desafios_cumpridos": qtd_d_cumpridos,"soli_desafios":qtd_soli_desafios, "d_ativos_desafiado":d_ativos_desafiado, "qtd_solicitacoes": qtd_solicitacoes
    
    insignias = Insignia.objects.filter()
    
    conq_u = []
    conquista = Conquista.objects.filter(usuario = u)
    
    for e in conquista:
        conq_u.append(e.insignia)
    
    return render(request, 'en/public/Conquistas.HTML' , {"conquista": conq_u, "insignias": insignias, "desafios_cumpridos": qtd_d_cumpridos,"soli_desafios":qtd_soli_desafios, "d_ativos_desafiado":d_ativos_desafiado,"Usuario":u, "qtd_solicitacoes": qtd_solicitacoes, "qtd_d_ativos_desafiado": qtd_d_ativos_desafiado,"pos_turma": pos_turma, "pos_geral": pos_geral,"qtd_msgs": qtd_msgs, "desafios_cumpridos": qtd_d_cumpridos,"soli_desafios":qtd_soli_desafios, "d_ativos_desafiado":d_ativos_desafiado, "qtd_solicitacoes": qtd_solicitacoes})

def Rankings (request):
    #---------------------------Notificações-----------------------------------------------------
    #Sessão do usuario
    u = Usuario.objects.filter(login=request.session['id']).get()
    #Quantidade de solicitações de amizade
    slct = Solicitacao.objects.filter(amigo=u)
    qtd_solicitacoes = len(slct)
    #Solicitações de desafios
    soli_desafios = Solicitacao_Desafio.objects.filter(usuario_desafiado = u)
    qtd_soli_desafios = len(soli_desafios)
    #Desafios Ativos
    d_ativos_desafiado = Desafio_Ativo.objects.filter(usuario_desafiado = u)
    #Desafios Cumpridos
    d_ativos_desafiante = Desafio_Ativo.objects.filter(usuario_desafiante = u, cumprido = True)
    qtd_d_cumpridos = len(d_ativos_desafiante)
    #Quantidade de Mensagens
    msgs = Mensagens.objects.filter(usuario = u)
    qtd_msgs = len(msgs)
    #{"desafios_cumpridos": qtd_d_cumpridos,"soli_desafios":qtd_soli_desafios, "d_ativos_desafiado":d_ativos_desafiado,"Usuario":u, "qtd_solicitacoes": qtd_solicitacoes}
    #----------------------------------------------------------------------------------------------
    
    qtd_d_ativos_desafiado = len(d_ativos_desafiado)
    ranking_geral = Usuario.objects.all().order_by('-pontos')
    lista_geral = list(ranking_geral)
    pos_geral = lista_geral.index(u) + 1
    
    ranking_turma = Usuario.objects.filter(turma = u.turma).order_by('-pontos')
    lista_turma = list(ranking_turma)
    pos_turma = lista_turma.index(u) + 1
    #"qtd_d_ativos_desafiado": qtd_d_ativos_desafiado,"pos_turma": pos_turma, "pos_geral": pos_geral,"qtd_msgs": qtd_msgs, "desafios_cumpridos": qtd_d_cumpridos,"soli_desafios":qtd_soli_desafios, "d_ativos_desafiado":d_ativos_desafiado, "qtd_solicitacoes": qtd_solicitacoes
    
    #ranking geral
    ranking = Usuario.objects.all().order_by('-pontos')
    
    return render(request, 'en/public/Rankings.HTML' ,{"ranking": ranking, "qtd_msgs":qtd_msgs,"desafios_cumpridos": qtd_d_cumpridos,"soli_desafios":qtd_soli_desafios, "d_ativos_desafiado":d_ativos_desafiado,"Usuario":u, "qtd_solicitacoes": qtd_solicitacoes, "qtd_d_ativos_desafiado": qtd_d_ativos_desafiado,"pos_turma": pos_turma, "pos_geral": pos_geral,"qtd_msgs": qtd_msgs, "desafios_cumpridos": qtd_d_cumpridos,"soli_desafios":qtd_soli_desafios, "d_ativos_desafiado":d_ativos_desafiado, "qtd_solicitacoes": qtd_solicitacoes})

def Rankings_Geral (request):
    
    #ranking geral
    ranking = Usuario.objects.all().order_by('-pontos')
    
    return render(request, 'en/public/Ranks.HTML' , {"ranking": ranking})

def Rankings_Turma (request):
    u = Usuario.objects.filter(login=request.session['id']).get()
            
    #ranking por turma
    ranking = Usuario.objects.filter(turma = u.turma).order_by('-pontos')
    
    
    return render(request, 'en/public/Ranks.HTML' , {"ranking": ranking})

def Rankings_Amigos (request):
    
    u = Usuario.objects.filter(login=request.session['id']).get()
    #ranking por amigos
    meus_amigos = Amigos.objects.filter(dono = u)
    amigos = [] 
    
    for a in meus_amigos:
        amigos.append(a.amigo)
    
    ranking = amigos
        
    return render(request, 'en/public/Ranks.HTML' , {"ranking": ranking})

@csrf_exempt
def Desafiar_Amigo (request):
    #---------------------------Notificações-----------------------------------------------------
    #Sessão do usuario
    u = Usuario.objects.filter(login=request.session['id']).get()
    #Quantidade de solicitações de amizade
    slct = Solicitacao.objects.filter(amigo=u)
    qtd_solicitacoes = len(slct)
    #Solicitações de desafios
    soli_desafios = Solicitacao_Desafio.objects.filter(usuario_desafiado = u)
    qtd_soli_desafios = len(soli_desafios)
    #Desafios Ativos
    d_ativos_desafiado = Desafio_Ativo.objects.filter(usuario_desafiado = u)
    #Desafios Cumpridos
    d_ativos_desafiante = Desafio_Ativo.objects.filter(usuario_desafiante = u, cumprido = True)
    qtd_d_cumpridos = len(d_ativos_desafiante)
    #Quantidade de Mensagens
    msgs = Mensagens.objects.filter(usuario = u)
    qtd_msgs = len(msgs)
    #{"desafios_cumpridos": qtd_d_cumpridos,"soli_desafios":qtd_soli_desafios, "d_ativos_desafiado":d_ativos_desafiado,"Usuario":u, "qtd_solicitacoes": qtd_solicitacoes}
    #----------------------------------------------------------------------------------------------
    
    id_amigo = request.POST["id_usuario"]
    
    amigo_desafiado = Usuario.objects.filter(id = id_amigo).get()
   
    #Busca de desafios e de Amigos
    desafios = Desafio.objects.all() 
    
    #Consulta para mostrar as solicitações
    soli_desafios = Solicitacao_Desafio.objects.filter(usuario_desafiado = u)
    #Notificação da quantidade de solicitação de desafios
    qtd_soli_desafios = len(soli_desafios)
    
    #Consulta para mostrar os desafios ativos
    d_ativos_desafiado = Desafio_Ativo.objects.filter(usuario_desafiado = u, enviado = False)
    
    #Consulta para mostrar os desafios cumpridos
    d_ativos_desafiante = Desafio_Ativo.objects.filter(usuario_desafiante = u, cumprido = True)
       
    return render(request, 'en/public/Desafios_Individual.HTML', {"qtd_msgs":qtd_msgs,"amigo": amigo_desafiado,"d_ativos_desafiante": d_ativos_desafiante, "d_ativos_desafiado": d_ativos_desafiado, "solicit_desafios": soli_desafios, "soli_desafios": qtd_soli_desafios, "desafios": desafios, "desafios_cumpridos": qtd_d_cumpridos,"soli_desafios":qtd_soli_desafios, "d_ativos_desafiado":d_ativos_desafiado,"Usuario":u, "qtd_solicitacoes": qtd_solicitacoes})

def Mensagens_Usuario (request):
     #---------------------------Notificações-----------------------------------------------------
    #Sessão do usuario
    u = Usuario.objects.filter(login=request.session['id']).get()
    #Quantidade de solicitações de amizade
    slct = Solicitacao.objects.filter(amigo=u)
    qtd_solicitacoes = len(slct)
    #Solicitações de desafios
    soli_desafios = Solicitacao_Desafio.objects.filter(usuario_desafiado = u)
    qtd_soli_desafios = len(soli_desafios)
    #Desafios Ativos
    d_ativos_desafiado = Desafio_Ativo.objects.filter(usuario_desafiado = u)
    #Desafios Cumpridos
    d_ativos_desafiante = Desafio_Ativo.objects.filter(usuario_desafiante = u, cumprido = True)
    qtd_d_cumpridos = len(d_ativos_desafiante)
    #{"desafios_cumpridos": qtd_d_cumpridos,"soli_desafios":qtd_soli_desafios, "d_ativos_desafiado":d_ativos_desafiado,"Usuario":u, "qtd_solicitacoes": qtd_solicitacoes}
    #----------------------------------------------------------------------------------------------
    
    msgs = Mensagens.objects.filter(usuario = u)
    qtd_msgs = len(msgs)
    return render(request, 'en/public/Mensagens.HTML', {"qtd_msgs": qtd_msgs, "msg_usuario": msgs, "desafios_cumpridos": qtd_d_cumpridos,"soli_desafios":qtd_soli_desafios, "d_ativos_desafiado":d_ativos_desafiado,"Usuario":u, "qtd_solicitacoes": qtd_solicitacoes})



def Apagar_Menagem (request):
     #---------------------------Notificações-----------------------------------------------------
    #Sessão do usuario
    u = Usuario.objects.filter(login=request.session['id']).get()
    #Quantidade de solicitações de amizade
    slct = Solicitacao.objects.filter(amigo=u)
    qtd_solicitacoes = len(slct)
    #Solicitações de desafios
    soli_desafios = Solicitacao_Desafio.objects.filter(usuario_desafiado = u)
    qtd_soli_desafios = len(soli_desafios)
    #Desafios Ativos
    d_ativos_desafiado = Desafio_Ativo.objects.filter(usuario_desafiado = u)
    #Desafios Cumpridos
    d_ativos_desafiante = Desafio_Ativo.objects.filter(usuario_desafiante = u, cumprido = True)
    qtd_d_cumpridos = len(d_ativos_desafiante)
    #Mensagens
    
    #{"desafios_cumpridos": qtd_d_cumpridos,"soli_desafios":qtd_soli_desafios, "d_ativos_desafiado":d_ativos_desafiado,"Usuario":u, "qtd_solicitacoes": qtd_solicitacoes}
    #----------------------------------------------------------------------------------------------
   
    id_mensagem = request.POST["cMensagem"]
    del_msg = Mensagens.objects.filter(id = id_mensagem).get()
    del_msg.delete()
    
    msgs = Mensagens.objects.filter(usuario = u)
    qtd_msgs = len(msgs)
    
    return render(request, 'en/public/Mensagens.HTML', {"qtd_msgs": qtd_msgs, "msg_usuario": msgs, "desafios_cumpridos": qtd_d_cumpridos,"soli_desafios":qtd_soli_desafios, "d_ativos_desafiado":d_ativos_desafiado,"Usuario":u, "qtd_solicitacoes": qtd_solicitacoes})


@csrf_exempt
def Pingo_Like (request):
    
    u = Usuario.objects.filter(login=request.session['id']).get()
    
    id_post = request.POST["cID_post"]
    
    post = TimeLine.objects.filter(id = id_post).get()
    post.qtd_pingo = post.qtd_pingo + 1
    post.save()
    
    pingo = Pingo(usuario = u, postagem = post)
    pingo.save()
  
    return HttpResponse(post.qtd_pingo)

@csrf_exempt
def Despingo_Deslike (request):
    u = Usuario.objects.filter(login=request.session['id']).get()
    
    id_post = request.POST["cID_post"]
    
    post = TimeLine.objects.filter(id = id_post).get()
    post.qtd_pingo = post.qtd_pingo - 1
    post.save()
    
    pingo = Pingo.objects.filter(usuario = u, postagem = post).get()
    pingo.delete()
  
    
    return HttpResponse(post.qtd_pingo)

def Atribuir_Conquistas(request, usu, dsf):
    
    u = usu   

    pesquisa_amigos = Amigos.objects.filter(dono=u)
    qtd_amigos = len(pesquisa_amigos)  

    try: #Conquista 1 - Feito
        
        i = Insignia.objects.filter(nome='Conquista 1').get()
        conq = Conquista.objects.filter(insignia=i, usuario=u).get()
     
    except:
        
        if(u.pontos >= 40):
            
                i = Insignia.objects.filter(nome='Conquista 1').get()
                conquista = Conquista(insignia = i, usuario=u)
                conquista.save()
            
    try:    #Conquista 2 - Feito
            
        i = Insignia.objects.filter(nome='Conquista 8').get()
        conq = Conquista.objects.filter(insignia=i, usuario=u).get()
            
    except:
        
        if(qtd_amigos >= 300):
            i = Insignia.objects.filter(nome='Conquista 8').get()
            conquista = Conquista(insignia = i, usuario = u)
            conquista.save()
            
    try:    #Conquista 3 - Feito
            
        i = Insignia.objects.filter(nome='Conquista 2').get()
        conq = Conquista.objects.filter(insignia=i, usuario=u).get()
            
    except:
        
        ucs = Usu_Comp_Semanal.objects.filter(usuario = u).get()
        
        data_atual = timezone.now()
            
        if(ucs.data_fim < data_atual and ucs.qtd_desafios >= 5):
                
            i = Insignia.objects.filter(nome='Conquista 2').get()
            conquista = Conquista(insignia = i, usuario = u)
            conquista.save()
                    
    try:    #Conquista 4 - Feito
            
        i = Insignia.objects.filter(nome='Conquista 4').get()
        conq = Conquista.objects.filter(insignia=i, usuario=u).get()
            
    except:
        
        if(u.pontos >= 80): 
            i = Insignia.objects.filter(nome='Conquista 4').get()
            conquista = Conquista(insignia=i, usuario=u)
            conquista.save()
                    
    try:    #Conquista 5 - Feito
            
        i = Insignia.objects.filter(nome='Conquista 5').get()
        conq = Conquista.objects.filter(insignia=i, usuario=u).get()
                        
    except:
                    
        if(dsf.desafio.nome == "Áquario"): 
            
            i = Insignia.objects.filter(nome='Conquista 5').get()
            conquista = Conquista(insignia = i, usuario = u)
            conquista.save()
                        
    try:    #Conquista 6
            
        i = Insignia.objects.filter(nome='Conquista 8').get()
        conq = Conquista.objects.filter(insignia=i, usuario=u).get()
                            
    except:
                        
        if(qtd_amigos >= 3):
            i = Insignia.objects.filter(nome='Conquista 8').get()
            conquista = Conquista(insignia = i, usuario = u)
            conquista.save()
                        
    try:    #Conquista 7
                
        i = Insignia.objects.filter(nome='Conquista 8').get()
        conq = Conquista.objects.filter(insignia=i, usuario=u).get()
                                
    except:
                            
        if(qtd_amigos >= 3):
            i = Insignia.objects.filter(nome='Conquista 8').get()
            conquista = Conquista(insignia = i, usuario = u)
            conquista.save()
                                    
    try:    #Conquista 8
            
        i = Insignia.objects.filter(nome='Conquista 8').get()
        conq = Conquista.objects.filter(insignia=i, usuario=u).get()
                                
    except:
                            
        if(qtd_amigos >= 3):
            i = Insignia.objects.filter(nome='Conquista 8').get()
            conquista = Conquista(insignia = i, usuario = u)
            conquista.save()
                                
    try:    #Conquista 9 - Feito
            
        i = Insignia.objects.filter(nome='Conquista 9').get()
        conq = Conquista.objects.filter(insignia=i, usuario=u).get()
            
    except:
        
        if(u.pontos >= 120):
            i = Insignia.objects.filter(nome='Conquista 9').get()
            conquista = Conquista(insignia = i, usuario = u)
            conquista.save() 
                                    
    try:    #Conquista 10
            
        i = Insignia.objects.filter(nome='Conquista 8').get()
        conq = Conquista.objects.filter(insignia=i, usuario=u).get()
                                            
    except:
                                        
        if(qtd_amigos >= 3):
            i = Insignia.objects.filter(nome='Conquista 8').get()
            conquista = Conquista(insignia = i, usuario = u)
            conquista.save()
                                            
    try:    #Conquista 11
            
        i = Insignia.objects.filter(nome='Conquista 8').get()
        conq = Conquista.objects.filter(insignia=i, usuario=u).get()
            
    except:
        
        if(qtd_amigos >= 3):
            i = Insignia.objects.filter(nome='Conquista 8').get()
            conquista = Conquista(insignia = i, usuario = u)
            conquista.save()
                                                                                    
    return Timeline(request)  

@csrf_exempt
def Usuarios_curtiram (request):
    #---------------------------Notificações-----------------------------------------------------
    #Sessão do usuario
    u = Usuario.objects.filter(login=request.session['id']).get()
    #Quantidade de solicitações de amizade
    slct = Solicitacao.objects.filter(amigo=u)
    qtd_solicitacoes = len(slct)
    #Solicitações de desafios
    soli_desafios = Solicitacao_Desafio.objects.filter(usuario_desafiado = u)
    qtd_soli_desafios = len(soli_desafios)
    #Desafios Ativos
    d_ativos_desafiado = Desafio_Ativo.objects.filter(usuario_desafiado = u)
    #Desafios Cumpridos
    d_ativos_desafiante = Desafio_Ativo.objects.filter(usuario_desafiante = u, cumprido = True)
    qtd_d_cumpridos = len(d_ativos_desafiante)
    #Mensagens
    
    id_post = request.POST["cID_post"]
    
    post = TimeLine.objects.filter(id = id_post).get()
    
    pingo = Pingo.objects.filter(postagem = post)
  
    return render(request, 'en/public/U_Curtiu.HTML', {"pingo": pingo, "desafios_cumpridos": qtd_d_cumpridos,"soli_desafios":qtd_soli_desafios, "d_ativos_desafiado":d_ativos_desafiado,"Usuario":u, "qtd_solicitacoes": qtd_solicitacoes})
    
@csrf_exempt
def Mais_posts (request):
    id_ultimo = request.POST["id_ultimo"]
    
    u = Usuario.objects.filter(login=request.session['id']).get()
    
    entr = TimeLine.objects.all().order_by('-date')
    
    postagem = TimeLine.objects.filter(id = id_ultimo).get()
    
    entries = list(entr)
    
    pos = entries.index(postagem) + 1
    
    qtd_entries = []
    
    
    i = 0
    for a in range(pos, len(entries)):
        
        try:
            pingo = Pingo.objects.filter(usuario = u, postagem = entries[a]).get()
            entries[a].curtiu = True
            entries[a].save()
        except:
            entries[a].curtiu = False       
            entries[a].save()
            
        qtd_entries.append(entries[a]) 
        i = i + 1
        
        if(i == 10):
            break

            
   
    return render_to_response('en/public/Feeds2.HTML', {"entries": qtd_entries, "Usuario":u})    
    
def Descurtir(request):
    return render(request, 'en/public/Descutir.HTML')

def Curtir(request):
    return render(request, 'en/public/Curtir.HTML')