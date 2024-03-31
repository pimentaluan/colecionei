from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from colecoes.forms import ColecaoForms, ItemForms
from usuarios.models import Usuario
from colecoes.models import Colecao, Item
from django.db import IntegrityError
from random import choice


def feed(request):
    user = request.user

    if not request.user.is_authenticated:
        messages.error(request, 'Usuário não logado')
        return redirect('login')

    icone = icone_aleatorio()
    
    return render(request, 'colecoes/feed.html', {'user': user, 'icone_aleatorio': icone})

def colecao(request, username, colecao_id):
    usuario = get_object_or_404(Usuario, username=username)
    colecao = get_object_or_404(Colecao, usuario=usuario, id=colecao_id)

    icone = icone_aleatorio()
    return render(request, 'colecoes/colecao.html', {'user': usuario, 'colecao': colecao, 'icone_aleatorio': icone})

def nova_colecao(request):
    if not request.user.is_authenticated:
        messages.error(request, 'Usuário não logado')
        return redirect('login')

    if request.method == 'POST':
        form = ColecaoForms(request.POST)
        if form.is_valid():
            colecao = form.save(commit=False)
            colecao.usuario = request.user
            try:
                colecao.save()
            except IntegrityError:
                messages.error(request, 'Uma coleção com esse nome já existe para este usuário.')
                return render(request, 'colecoes/nova_colecao.html', {'user': request.user, 'form': form})
            messages.success(request, 'Coleção criada com sucesso')
            return redirect('feed')
    else:
        form = ColecaoForms()
    
    icone = icone_aleatorio()

    return render(request, 'colecoes/nova_colecao.html', {'user': request.user, 'form': form, 'icone_aleatorio': icone})

def novo_item(request, username, colecao_id):
    usuario = get_object_or_404(Usuario, username=username)
    colecao = get_object_or_404(Colecao, usuario=usuario, id=colecao_id)

    if request.user != usuario:
        messages.error(request, 'Você não tem permissão para adicionar um item a esta coleção.')
        return redirect('feed')

    if request.method == 'POST':
        form = ItemForms(request.POST, request.FILES)
        if form.is_valid():
            item = form.save(commit=False)
            item.colecao = colecao
            item.save()
            return redirect('feed')
    else:
        form = ItemForms()

    icone = icone_aleatorio()
    return render(request, 'colecoes/novo_item.html', {'form': form, 'colecao': colecao, 'icone_aleatorio': icone})

def perfil(request, usuario_id):
    if not request.user.is_authenticated:
        messages.error(request, 'Usuário não logado')
        return redirect('login')
    
    user = request.user
    colecoes = Colecao.objects.filter(usuario=user)
    quantidade_colecoes = colecoes.count()

    itens = Item.objects.filter(colecao__usuario=user)
    quantidade_itens = itens.count()
    icone = icone_aleatorio()

    return render(request, 'colecoes/perfil.html', {'user': user, 'colecoes': colecoes, 'quantidade_colecoes': quantidade_colecoes, 'quantidade_itens':quantidade_itens , 'icone_aleatorio': icone})

def icone_aleatorio():
    icones = ['fantasma.svg', 'caveira.svg', 'foguete.svg']
    icone_aleatorio = choice(icones)
    return icone_aleatorio

def buscar(request):
    if not request.user.is_authenticated:
        messages.error(request, 'Usuário não logado')
        return redirect('login')
    query = request.GET.get('buscar')
    if query:
        usuarios = Usuario.objects.filter(username__icontains=query)
        colecoes = Colecao.objects.filter(nome__icontains=query)
        itens = Item.objects.filter(nome__icontains=query)
    else:
        usuarios = Usuario.objects.none()
        colecoes = Colecao.objects.none()
        itens = Item.objects.none()
    icone = icone_aleatorio()

    for usuario in usuarios:
        usuario.esta_seguindo = request.user.esta_seguindo(usuario)

    return render(request, 'colecoes/busca.html', {'user': request.user, 'usuarios': usuarios, 'colecoes': colecoes, 'itens': itens, 'icone_aleatorio': icone})