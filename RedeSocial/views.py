from RedeSocial.models import TimeLine, Usuario
from django.views.generic.base import TemplateView

def formPostagem(request):
    if request.POST:
        form = TimeLine(request.POST)
        form1 = TimeLine(request.FILES)
        form2 = TimeLine(request.POST, request.FILES)
        
        if form.valid():
            form.save()
           
        
        elif form1.valid():
            form1.save() 
           
        
        elif form2.valid():
            form2.save()

def formEditarPerfil(request):
    if request.POST:
        form2 = Usuario(request.POST, request.FILES)
        
        if form2.valid():
            form2.save()

    
