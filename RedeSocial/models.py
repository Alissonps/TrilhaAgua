from django.db import models

class Competicao(models.Model):
    id = models.IntegerField(primary_key = True)
    data_inicio = models.DateTimeField()
    data_fim = models.DateTimeField()
    ativo = models.BooleanField(blank=True, default=False)
     
    def __str__(self):
        return "id: %s - fim: %s" % (self.id, self.data_fim)
    
class Usuario (models.Model):
    id = models.IntegerField(primary_key=True)
    login = models.CharField(max_length=40)
    senha = models.CharField(max_length=40)
    nome = models.CharField(max_length=40)
    email = models.CharField(max_length=40)
    matricula = models.CharField(max_length=40)
    idade = models.IntegerField(max_length=3)
    turma = models.CharField(max_length=40)
    sexo = models.CharField(max_length=40)
    pergunta = models.CharField(max_length=40)
    resposta = models.CharField(max_length=40)
    descricao = models.TextField()
    foto = models.ImageField(blank=True, null=True, default=False, upload_to='media')
    pontos = models.IntegerField(blank=True, null=True, default = 0)
    professor = models.BooleanField(blank = True, default = None)
    
    
    def __str__(self):
        return "Nome: %s - Login: %s" % (self.nome, self.login)
    

class hist_pontuacao (models.Model):
    usuario = models.ForeignKey(Usuario)
    pontuacao = models.IntegerField(max_length = 10)
    competicao = models.ForeignKey(Competicao)
    
    def __str__(self):
        return "Nome: %s - pontuacao: %s" % (self.usuario, self.pontuacao)

class TimeLine (models.Model):
    id = models.IntegerField(primary_key=True)
    date = models.DateTimeField(auto_now_add=True)
    text = models.TextField()
    usuario = models.ForeignKey(Usuario)
    foto = models.ImageField(blank=True, null=True, default=False, upload_to='media')
    qtd_coments = models.IntegerField(max_length=10, blank=True, null=True, default=0)
    nome_desafio = models.CharField(max_length=10, blank=True, null=True, default=None)
    desafio = models.BooleanField(blank=True, default=False)
    competicao = models.ForeignKey(Competicao, null=True, default=None)
    qtd_pingo = models.IntegerField(max_length=10, blank=True, null=True, default=0)
    curtiu = models.BooleanField(blank=True, default=False)
    
    def __str__(self):
        return "Id: %s" % (self.id)
    
class Beta_TimeLine (models.Model):
    id = models.IntegerField(primary_key=True)
    date = models.DateTimeField(auto_now_add=True)
    text = models.TextField()
    usuario = models.ForeignKey(Usuario)
    foto = models.ImageField(blank=True, null=True, default=False, upload_to='media')
    qtd_coments = models.IntegerField(max_length=10, blank=True, null=True, default=0)
    nome_desafio = models.CharField(max_length=10, blank=True, null=True, default=None)
    desafio = models.BooleanField(max_length=10, blank=True, default=False)
    competicao = models.ForeignKey(Competicao, null=True, default=None)
    qtd_pingo = models.IntegerField(max_length=10, blank=True, null=True, default=0)
    
    def __str__(self):
        return "Id: %s" % (self.id)

class Comentarios (models.Model):
    text = models.TextField()
    usuario = models.ForeignKey(Usuario)
    postagem = models.ForeignKey(TimeLine, null=True)
    date = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return "Usuario: %s - Postagem: %s" % (self.usuario, self.postagem)
        
class Solicitacao(models.Model):
    id = models.IntegerField(primary_key = True)
    usuario = models.ForeignKey(Usuario, related_name="Remetente", null=True, default=None)
    amigo = models.ForeignKey(Usuario, related_name="Destinatario", null=True, default=None)
    resposta = models.BooleanField(default=None)
    
    def __str__(self):
        return "O remetente: %s solicitou o Amigo: %s" % (self.usuario.nome, self.amigo.nome)
    
class Amigos(models.Model):
    id = models.IntegerField(primary_key = True)
    dono = models.ForeignKey(Usuario, null=True, default=None)
    amigo = models.ForeignKey(Usuario, related_name="Amigo", null=True, default=None)
    
    def __str__(self):
        return "Proprietario: %s Turma: %s ,Amigo: %s" % (self.dono.nome, self.dono.turma, self.amigo.nome)

class Desafio(models.Model):
    
    id = models.IntegerField(primary_key = True)
    nome = models.CharField(max_length = 30)
    descricao = models.TextField()
    pontuacao = models.IntegerField(max_length = 3)
    
    def __str__(self):
        return " %s : %s pontos" % (self.nome, self.pontuacao)
    
class Solicitacao_Desafio(models.Model):
    
    id = models.IntegerField(primary_key = True)
    usuario_desafiante = models.ForeignKey(Usuario, related_name = "desafiante", null=True, default=None)
    usuario_desafiado = models.ForeignKey(Usuario, related_name = "desafiado", null=True, default=None)
    desafio = models.ForeignKey(Desafio, related_name = "desafio", null=True, default=None)
    resposta = models.BooleanField(default=None)
    
    def __str__(self):
        return "O desafiante: %s desafiou: %s" % (self.usuario_desafiante.nome, self.usuario_desafiado.nome)
    

class Desafio_Ativo(models.Model):
    
    id = models.IntegerField(primary_key = True)
    usuario_desafiante = models.ForeignKey(Usuario, related_name = "TDesafio_desafiante", null=True, default=None, blank = True)
    usuario_desafiado = models.ForeignKey(Usuario, related_name = "TDesafio_desafiado", null=True, default=None, blank = True)
    postagem = models.ForeignKey(TimeLine, related_name = "TDesafio_postagem", null = True, blank = True)
    desafio = models.ForeignKey(Desafio, related_name = "TDesafio", null=True, default=None, blank = True)
    cumprido = models.BooleanField(blank = True, default = None)
    enviado = models.BooleanField(blank = True, default = None)
    
    def __str__(self):
        return "%s - %s - %s to %s" % (self.id, self.usuario_desafiante, self.desafio, self.usuario_desafiado)

class Cont_Postagem(models.Model):
    id = models.IntegerField(primary_key = True)
    qtd = models.IntegerField(blank = True, null = True, default = 0)
    
    def __str__(self):
        return "Qtd: %s" % (self.qtd)
    
class Mensagens(models.Model):
    id = models.IntegerField(primary_key = True)
    usuario = models.ForeignKey(Usuario) 
    mensagem = models.CharField(max_length = 100)
    
    def __str__(self):
        return "%s" % (self.usuario)
        
class Campeao(models.Model):
    id = models.IntegerField(primary_key = True)
    mes = models.IntegerField()
    usuario = models.ForeignKey(Usuario)
    pontuacao = models.IntegerField(max_length = 10)
    geral = models.BooleanField(blank = True, default = None)
    turma = models.BooleanField(blank = True, default = None)
    
    def __str__(self):
        return "%s" % (self.mes)
    
class Pingo (models.Model):
    usuario = models.ForeignKey(Usuario)
    postagem = models.ForeignKey(TimeLine)
       
    def __str__(self):
        return "Usuario: %s - Postagem: %s" % (self.usuario, self.postagem)

class Insignia(models.Model):
    
    nome = models.CharField(max_length = 30)
    Imagem = models.ImageField(blank=True, null=True, default=False, upload_to='media')
    descricao = models.TextField()
    
    def __str__(self):
        return "Nome: %s" % (self.nome)
    
    
class Conquista(models.Model):
    insignia = models.ForeignKey(Insignia)
    usuario = models.ForeignKey(Usuario)
    
    def __str__(self):
        return "Usuario: %s - Postagem: %s" % (self.usuario, self.insignia)