from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.utils import timezone
from colecoes.forms import ColecaoForms, ItemForms, EditarPerfilForm
from usuarios.models import Usuario
from colecoes.models import Colecao, Item, Comentario, Busca
from django.db import IntegrityError
from random import choice
from itertools import chain
from django.core.paginator import Paginator
from django.db.models import Count
from random import sample



def pagina_anterior(request):
    return request.META.get('HTTP_REFERER')

def feed(request):
    if not request.user.is_authenticated:
        messages.error(request, 'Usuário não logado')
        return redirect('login')

    user = request.user
    icone = icone_aleatorio()

    # Usuários seguidos
    usuarios_seguidos = user.seguindo.all()

    # Coleções dos usuários seguidos (mais relevantes primeiro)
    colecoes_seguidas = Colecao.objects.filter(usuario__in=usuarios_seguidos).annotate(
        likes_count=Count('likes')
    ).order_by('-likes_count', '-data_criacao')

    # Recomendações de coleções
    categorias_interessadas = Item.objects.filter(colecao__usuario=user).values_list('categoria', flat=True)
    recomendacoes_colecoes = Colecao.objects.filter(categoria__in=categorias_interessadas).exclude(usuario=user).annotate(
        likes_count=Count('likes')
    ).order_by('-likes_count', '-data_criacao')[:10]

    # Recomendações de perfis esporádicas
    usuarios_nao_seguidos = Usuario.objects.exclude(id__in=usuarios_seguidos).exclude(id=user.id)
    num_usuarios_para_recomendar = min(3, len(usuarios_nao_seguidos))
    recomendacoes_usuarios = sample(list(usuarios_nao_seguidos), num_usuarios_para_recomendar)

    # Adicionando uma marcação de tipo para recomendação de usuário
    recomendacoes_usuarios = [{'tipo': 'usuario', 'usuario': usuario} for usuario in recomendacoes_usuarios]

    # Combinar coleções seguidas e recomendações em um único feed
    feed_items = sorted(
        chain(colecoes_seguidas, recomendacoes_colecoes, recomendacoes_usuarios),
        key=lambda obj: obj.data_criacao if hasattr(obj, 'data_criacao') else timezone.now(),
        reverse=True
    )

    paginator = Paginator(feed_items, 10)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    return render(request, 'colecoes/feed.html', {
        'user': user,
        'icone_aleatorio': icone,
        'feed_items': page_obj,
    })



def colecao(request, username, colecao_id):
    user = request.user
    usuario = get_object_or_404(Usuario, username=username)
    colecao = get_object_or_404(Colecao, usuario=usuario, id=colecao_id)
    likes_count = colecao.get_likes_count()

    user_has_liked = False
    user_has_saved = False
    if user.is_authenticated:
        user_has_liked = colecao.likes.filter(id=user.id).exists()
        user_has_saved = user.colecoes_salvas.filter(id=colecao_id).exists()

    icone = icone_aleatorio()
    
    url_pagina_anterior = pagina_anterior(request)
    return render(request, 'colecoes/colecao.html', {'user': user, 'username': username, 'colecao_id': colecao_id, 'colecao': colecao, 'icone_aleatorio': icone, 'likes_count': likes_count, 'user_has_liked': user_has_liked, 'user_has_saved': user_has_saved, 'pagina_anterior': url_pagina_anterior})

def nova_colecao(request):
    if not request.user.is_authenticated:
        messages.error(request, 'Usuário não logado')
        return redirect('login')

    if request.method == 'POST':
        form = ColecaoForms(request.POST, request.FILES)
        if form.is_valid():
            colecao = form.save(commit=False)
            colecao.usuario = request.user
            try:
                colecao.save()
            except IntegrityError:
                messages.error(request, 'Uma coleção com esse nome já existe para este usuário.')
                return render(request, 'colecoes/nova_colecao.html', {'user': request.user, 'form': form})
            messages.success(request, 'Coleção criada com sucesso')
            return redirect('perfil', usuario_id=request.user.username)
    else:
        form = ColecaoForms()
    
    icone = icone_aleatorio()

    return render(request, 'colecoes/nova_colecao.html', {'user': request.user, 'form': form, 'icone_aleatorio': icone})

def novo_item(request, username, colecao_id):
    if not request.user.is_authenticated:
        messages.error(request, 'Usuário não logado')
        return redirect('login')
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
            return redirect('colecao', username=username, colecao_id=colecao_id)
    else:
        form = ItemForms()

    icone = icone_aleatorio()
    return render(request, 'colecoes/novo_item.html', {'form': form, 'colecao': colecao, 'icone_aleatorio': icone})

def meu_perfil(request):
    if not request.user.is_authenticated:
        messages.error(request, 'Usuário não logado')
        return redirect('login')
    
    user = request.user
    colecoes = Colecao.objects.filter(usuario=user)
    quantidade_colecoes = colecoes.count()

    itens = Item.objects.filter(colecao__usuario=user)
    quantidade_itens = itens.count()
    icone = icone_aleatorio()
    
    for colecao in colecoes:
        if colecao.cor in ['#FFCA2C', '#D9C95B', '#D9AA5B', '#D9D2A3', '#A3A3D9']:
            colecao.texto_preto = True
        else:
            colecao.texto_preto = False
            
    quantidade_seguindo = user.seguindo.count()
    quantidade_seguidores = user.seguidores.count()
        
    return render(request, 'colecoes/meu-perfil.html', {
            'other_user': user,
            'colecoes': colecoes,
            'quantidade_colecoes': quantidade_colecoes,
            'quantidade_itens': quantidade_itens,
            'icone_aleatorio': icone,
            'quantidade_seguindo': quantidade_seguindo,
            'quantidade_seguidores': quantidade_seguidores,
        })
    

def editar_perfil(request, username):
    if not request.user.is_authenticated:
        messages.error(request, 'Usuário não logado')
        return redirect('login')
    user = get_object_or_404(Usuario, username=username)
    if request.method == 'POST':
        form = EditarPerfilForm(request.POST, request.FILES, instance=user)
        if form.is_valid():
            form.save()
            messages.success(request, 'Perfil atualizado com sucesso')
            return redirect('meu-perfil')
        else:
            messages.error(request, 'Por favor, corrija os erros abaixo.')
    else:
        form = EditarPerfilForm(instance=user)
    return render(request, 'colecoes/editar_perfil.html', {'form': form})

def perfil(request, username):
    user = request.user
    other_user = get_object_or_404(Usuario, username=username)
    if request.user != other_user:
        colecoes = Colecao.objects.filter(usuario=other_user)
        quantidade_colecoes = colecoes.count()
        itens = Item.objects.filter(colecao__usuario=other_user)
        quantidade_itens = itens.count()
        icone = icone_aleatorio()

        for colecao in colecoes:
            if colecao.cor in ['#FFCA2C', '#D9C95B', '#D9AA5B', '#D9D2A3', '#A3A3D9']:
                colecao.texto_preto = True
            else:
                colecao.texto_preto = False
    
        url_pagina_anterior = pagina_anterior(request)

        quantidade_seguindo = other_user.seguindo.count()
        quantidade_seguidores = other_user.seguidores.count()

        esta_seguindo = False
        if request.user.is_authenticated:
            esta_seguindo = request.user.esta_seguindo(other_user)
        
        return render(request, 'colecoes/perfil.html', {
            'other_user': other_user,
            'colecoes': colecoes,
            'quantidade_colecoes': quantidade_colecoes,
            'quantidade_itens': quantidade_itens,
            'icone_aleatorio': icone,
            'pagina_anterior': url_pagina_anterior,
            'quantidade_seguindo': quantidade_seguindo,
            'quantidade_seguidores': quantidade_seguidores,
            'esta_seguindo': esta_seguindo,
        })
    else:
        return meu_perfil(request)

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

        busca = Busca.objects.filter(usuario=request.user, query=query).order_by('-data_hora').first()
        if busca is None:
            busca = Busca.objects.create(usuario=request.user, query=query)
        else:
            busca.data_hora = timezone.now()
            busca.save()
    else:
        usuarios = Usuario.objects.none()
        colecoes = Colecao.objects.none()
        itens = Item.objects.none()
    icone = icone_aleatorio()

    for usuario in usuarios:
        usuario.esta_seguindo = request.user.esta_seguindo(usuario)

    historico_busca = Busca.objects.filter(usuario=request.user).order_by('-data_hora')

    quantidade_seguindo = request.user.seguindo.count()
    quantidade_seguidores = request.user.seguidores.count()
    
    return render(request, 'colecoes/busca.html', {'user': request.user, 'usuarios': usuarios, 'quantidade_seguindo': quantidade_seguindo, 'quantidade_seguidores': quantidade_seguidores, 'colecoes': colecoes, 'itens': itens, 'icone_aleatorio': icone, 'historico_busca': historico_busca})

def favoritos(request):
    if not request.user.is_authenticated:
        messages.error(request, 'Usuário não logado')
        return redirect('login')
    
    user = request.user
    colecoes_salvas = user.colecoes_salvas.all()
    icone = icone_aleatorio()

    return render(request, 'colecoes/favoritos.html', {'user': user, 'colecoes_salvas': colecoes_salvas, 'icone_aleatorio': icone})

def like_colecao(request, colecao_id):
    if not request.user.is_authenticated:
        messages.error(request, 'Usuário não logado')
        return redirect('login')
    
    user = request.user
    colecao = get_object_or_404(Colecao, id=colecao_id)

    user_has_liked = colecao.likes.filter(id=user.id).exists()

    if user_has_liked:
        colecao.likes.remove(user)
    else:
        colecao.likes.add(user)

    return redirect('colecao', username=colecao.usuario.username, colecao_id=colecao_id)

def salvar_colecao(request, colecao_id):
    if not request.user.is_authenticated:
        messages.error(request, 'Usuário não logado')
        return redirect('login')
    user = request.user
    colecao = get_object_or_404(Colecao, id=colecao_id)

    user_has_saved = user.colecoes_salvas.filter(id=colecao_id).exists()

    if user_has_saved:
        user.colecoes_salvas.remove(colecao)
    else:
        user.colecoes_salvas.add(colecao)

    return redirect('colecao', username=colecao.usuario.username, colecao_id=colecao_id)

def comentar_colecao(request, colecao_id):
    if not request.user.is_authenticated:
        messages.error(request, 'Usuário não logado')
        return redirect('login')
    colecao = get_object_or_404(Colecao, id=colecao_id)
    if request.method == 'POST':
        texto_comentario = request.POST.get('comentario')
        Comentario.objects.create(usuario=request.user, colecao=colecao, texto=texto_comentario)
    return redirect('colecao', username=colecao.usuario.username, colecao_id=colecao_id)

def seguindo(request, username):
    if not request.user.is_authenticated:
        messages.error(request, 'Usuário não logado')
        return redirect('login')
    user = get_object_or_404(Usuario, username=username)
    seguindo = user.seguindo.all()
    icone = icone_aleatorio()
    return render(request, 'colecoes/seguindo.html', {'user': user, 'seguindo': seguindo, 'icone_aleatorio': icone})

def seguidores(request, username):
    if not request.user.is_authenticated:
        messages.error(request, 'Usuário não logado')
        return redirect('login')
    
    user = get_object_or_404(Usuario, username=username)
    seguidores = user.seguidores.all()
    icone = icone_aleatorio()
    
    # Obter a lista de usuários que o usuário atual está seguindo
    esta_seguindo = request.user.seguindo.all()
    
    return render(request, 'colecoes/seguidores.html', {
        'user': user,
        'seguido': seguidores,
        'icone_aleatorio': icone,
        'esta_seguindo': esta_seguindo,
    })