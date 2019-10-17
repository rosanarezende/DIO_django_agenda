from django.shortcuts import render, redirect
from core.models import Evento
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages

# Create your views here.

# def index(request):
#     return redirect('/agenda/')

# @login_required(login_url='/login/')
# def delete_evento(request, id_evento):
#     Evento.objects.filter(id=id_evento).delete()
#     return redirect('/')

@login_required(login_url='/login/')
def delete_evento(request, id_evento):
    usuario = request.user
    evento = Evento.objects.get(id=id_evento)
    if usuario == evento.usuario:
        evento.delete()
    return redirect('/')

@login_required(login_url='/login/')
def submit_evento(request):
    if request.POST:
        titulo = request.POST.get('titulo')
        data_evento = request.POST.get('data_evento')
        descricao = request.POST.get('descricao')
        usuario = request.user
        local_evento = request.POST.get('local_evento')
        id_evento = request.POST.get('id_evento')
        if id_evento:
            # Evento.objects.filter(id=id_evento).update(titulo=titulo,
            #                                            data_evento=data_evento,
            #                                            descricao=descricao,
            #                                            local_evento=local_evento)
            evento = Evento.objects.get(id=id_evento)
            if usuario == evento.usuario:
                evento.titulo = titulo
                evento.data_evento = data_evento
                evento.descricao = descricao
                evento.local_evento = local_evento
                evento.save()
        else:
            Evento.objects.create(titulo=titulo,
                                  data_evento=data_evento,
                                  descricao=descricao,
                                  usuario=usuario,
                                  local_evento=local_evento)
    return redirect('/')

@login_required(login_url='/login/')
def evento(request):
    id_evento = request.GET.get('id')
    dados = {}
    if id_evento:
        dados['evento'] = Evento.objects.get(id=id_evento)
    return render (request, 'evento.html', dados)

def logout_user(request):
    logout(request)
    return redirect('/')

def submit_login(request):
    if request.POST:
        username = request.POST.get('username')
        password = request.POST.get('password')
        usuario = authenticate(username=username, password=password)
        if usuario is not None: #se não é vazio, faço login
            login(request, usuario)
            return redirect('/') #redireciona pro indice
        else:
            messages.error(request, "Usuário ou senha inválidos")
    return redirect('/') #como não tá autenticado, vai voltar pro login

def login_user(request):
    return render(request, 'login.html')

@login_required(login_url='/login/') #quando não tiver autenticado, me leva pra esse endereço
def lista_eventos(request):
    usuario = request.user
    evento = Evento.objects.filter(usuario=usuario) #all tratá uma lista
    dados = {'eventos': evento}
    return render(request, 'agenda.html', dados)