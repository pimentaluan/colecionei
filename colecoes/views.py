from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from colecoes.forms import ColecaoForms, ItemForms
from usuarios.models import Usuario
from colecoes.models import Colecao
from django.db import IntegrityError


def feed(request):
    user = request.user

    if not request.user.is_authenticated:
        messages.error(request, 'Usuário não logado')
        return redirect('login')
    
    return render(request, 'colecoes/feed.html', {'user': user})


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

    return render(request, 'colecoes/nova_colecao.html', {'user': request.user, 'form': form})

def novo_item(request, username, colecao_id):
    usuario = get_object_or_404(Usuario, username=username)
    colecao = get_object_or_404(Colecao, usuario=usuario, id=colecao_id)

    # Verifique se o usuário atual é o proprietário da coleção
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
    return render(request, 'colecoes/novo_item.html', {'form': form, 'colecao': colecao})