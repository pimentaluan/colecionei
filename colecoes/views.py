from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.utils import timezone
from colecoes.forms import ColecaoForms, ItemForms
from usuarios.models import Usuario
from colecoes.models import Colecao, Item, Comentario, Busca
from django.db import IntegrityError
from random import choice


def pagina_anterior(request):
    return request.META.get('HTTP_REFERER')

def feed(request):
    if not request.user.is_authenticated:
        messages.error(request, 'Usuário não logado')
        return redirect('login')

    user = request.user
    icone = icone_aleatorio()

    usuarios_seguidos = user.seguindo.all()
    colecoes_seguindo = Colecao.objects.filter(usuario__in=usuarios_seguidos).order_by('-data_criacao')
    
    stopwords = ['de', 'para', 'a', 'o', 'que', 'e', 'do', 'da', 'em', 'um', 'para', 'é', 'com', 'não', 'uma', 'os', 'no', 'se', 'na', 'por', 'mais', 'as', 'dos', 'como', 'mas', 'foi', 'ao', 'ele', 'das', 'tem', 'à', 'seu', 'sua', 'ou', 'ser', 'quando', 'muito', 'há', 'nos', 'já', 'está', 'eu', 'também', 'só', 'pelo', 'pela', 'até', 'isso', 'ela', 'entre', 'era', 'depois', 'sem', 'mesmo', 'aos', 'ter', 'seus', 'quem', 'nas', 'me', 'esse', 'eles', 'estão', 'você', 'tinha', 'foram', 'essa', 'num', 'nem', 'suas', 'meu', 'às', 'minha', 'têm', 'numa', 'pelos', 'elas', 'havia', 'seja', 'qual', 'será', 'nós', 'tenho', 'lhe', 'deles', 'essas', 'esses', 'pelas', 'este', 'fosse', 'dele', 'tu', 'te', 'vocês', 'vos', 'lhes', 'meus', 'minhas', 'teu', 'tua', 'teus', 'tuas', 'nosso', 'nossa', 'nossos', 'nossas', 'dela', 'delas', 'esta', 'estes', 'estas', 'aquele', 'aquela', 'aqueles', 'aquelas', 'isto', 'aquilo', 'estou', 'está', 'estamos', 'estão', 'estive', 'esteve', 'estivemos', 'estiveram', 'estava', 'estávamos', 'estavam', 'estivera', 'estivéramos', 'esteja', 'estejamos', 'estejam', 'estivesse', 'estivéssemos', 'estivessem', 'estiver', 'estivermos', 'estiverem', 'hei', 'há', 'havemos', 'hão', 'houve', 'houvemos', 'houveram', 'houvera', 'houvéramos', 'haja', 'hajamos', 'hajam', 'houvesse', 'houvéssemos', 'houvessem', 'houver', 'houvermos', 'houverem', 'houverei', 'houverá', 'houveremos', 'houverão', 'houveria', 'houveríamos', 'houveriam', 'sou', 'somos', 'são', 'era', 'éramos', 'eram', 'fui', 'foi', 'fomos', 'foram', 'fora', 'fôramos', 'seja', 'sejamos', 'sejam', 'fosse', 'fôssemos', 'fossem', 'for', 'formos', 'forem', 'serei', 'será', 'seremos', 'serão', 'seria', 'seríamos', 'seriam', 'tenho', 'tem', 'temos', 'tém', 'tinha', 'tínhamos', 'tinham', 'tive', 'teve', 'tivemos', 'tiveram', 'tivera', 'tivéramos', 'tenha', 'tenhamos', 'tenham', 'tivesse', 'tivéssemos', 'tivessem', 'tiver', 'tivermos', 'tiverem', 'terei', 'terá', 'teremos', 'terão', 'teria', 'teríamos', 'teriam']
    keywords = []
    
    for colecao in colecgitoes_seguindo:
        words = colecao.descricao.split()
    
        words = [word for word in words if word not in stopwords]
    
        keywords.extend(words)
    
    keywords.extend(colecoes_seguindo.values_list('nome', 'tags', flat=True))
    
    

    return render(request, 'colecoes/feed.html', {'user': user, 'icone_aleatorio': icone})

def colecao(request, username, colecao_id):
    if not request.user.is_authenticated:
        messages.error(request, 'Usuário não logado')
        return redirect('login')

    user = request.user
    usuario = get_object_or_404(Usuario, username=username)
    colecao = get_object_or_404(Colecao, usuario=usuario, id=colecao_id)
    likes_count = colecao.get_likes_count()

    user_has_liked = colecao.likes.filter(id=user.id).exists()
    user_has_saved = request.user.colecoes_salvas.filter(id=colecao_id).exists()

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
            return redirect('perfil', usuario_id=request.user.id)
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
    
def perfil(request, usuario_id):
    user = get_object_or_404(Usuario, pk=usuario_id)

    if request.user != user:
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
    
        url_pagina_anterior = pagina_anterior(request)

        quantidade_seguindo = user.seguindo.count()
        quantidade_seguidores = user.seguidores.count()
        
        return render(request, 'colecoes/perfil.html', {
        'other_user': user,
        'colecoes': colecoes,
        'quantidade_colecoes': quantidade_colecoes,
        'quantidade_itens': quantidade_itens,
        'icone_aleatorio': icone,
        'pagina_anterior': url_pagina_anterior,
        'quantidade_seguindo': quantidade_seguindo,
        'quantidade_seguidores': quantidade_seguidores,
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

    return render(request, 'colecoes/busca.html', {'user': request.user, 'usuarios': usuarios, 'colecoes': colecoes, 'itens': itens, 'icone_aleatorio': icone, 'historico_busca': historico_busca})

def favoritos(request):
    if not request.user.is_authenticated:
        messages.error(request, 'Usuário não logado')
        return redirect('login')
    
    user = request.user
    colecoes_salvas = user.colecoes_salvas.all()
    icone = icone_aleatorio()

    return render(request, 'colecoes/favoritos.html', {'user': user, 'colecoes_salvas': colecoes_salvas, 'icone_aleatorio': icone})

def like_colecao(request, colecao_id):
    user = request.user
    colecao = get_object_or_404(Colecao, id=colecao_id)

    user_has_liked = colecao.likes.filter(id=user.id).exists()

    if user_has_liked:
        colecao.likes.remove(user)
    else:
        colecao.likes.add(user)

    return redirect('colecao', username=colecao.usuario.username, colecao_id=colecao_id)

def salvar_colecao(request, colecao_id):
    user = request.user
    colecao = get_object_or_404(Colecao, id=colecao_id)

    user_has_saved = user.colecoes_salvas.filter(id=colecao_id).exists()

    if user_has_saved:
        user.colecoes_salvas.remove(colecao)
    else:
        user.colecoes_salvas.add(colecao)

    return redirect('colecao', username=colecao.usuario.username, colecao_id=colecao_id)

def comentar_colecao(request, colecao_id):
    colecao = get_object_or_404(Colecao, id=colecao_id)
    if request.method == 'POST':
        texto_comentario = request.POST.get('comentario')
        Comentario.objects.create(usuario=request.user, colecao=colecao, texto=texto_comentario)
    return redirect('colecao', username=colecao.usuario.username, colecao_id=colecao_id)