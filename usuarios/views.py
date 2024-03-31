from django.shortcuts import render, redirect, get_object_or_404
from usuarios.forms import LoginForms, CadastroForms
from usuarios.models import Usuario
from django.contrib import auth, messages

def login(request):
    form = LoginForms()

    if request.method == 'POST':
        form = LoginForms(request.POST)

        if form.is_valid():
            nome = form.cleaned_data["nome_login"]
            senha = form.cleaned_data["senha"]

            usuario = auth.authenticate(
                request,
                username=nome,
                password=senha,
            )
            if usuario is not None:
                auth.login(request, usuario)
                messages.success(request, f'{nome} logado com sucesso!')
                return redirect('feed')
            else:
                messages.error(request, f'{nome} erro ao efetuar login!')
                return redirect('login')

    return render(request, "usuarios/login.html", {"form": form})

def cadastro(request):
    form = CadastroForms()

    if request.method == 'POST':
        form = CadastroForms(request.POST)

        if form.is_valid():
            if form.cleaned_data["senha_1"] != form.cleaned_data["senha_2"]:
                messages.error(request, f'As senhas não são iguais!')
                return redirect('cadastro')

            nome_completo = form.cleaned_data["nome_completo_cadastro"]
            email = form.cleaned_data["email"]
            senha = form.cleaned_data["senha_1"]
            username = form.cleaned_data["nome_cadastro"]

            if Usuario.objects.filter(username=username).exists():
                username = f"{username}_{Usuario.objects.count() + 1}"

            usuario = Usuario.objects.create_user(
                username=username,
                email=email,
                password=senha
            )
            usuario.nome_completo = nome_completo

            usuario.save()

            messages.success(request, f'{nome_completo} cadastrado com sucesso!')
            return redirect('login')
    return render(request, "usuarios/cadastro.html", {"form": form})

def logout(request):
    auth.logout(request)
    messages.success(request, 'Logout efetuado com sucesso!')
    return redirect('login')

def seguir_usuario(request, usuario_id):
    usuario_a_seguir = get_object_or_404(Usuario, id=usuario_id)
    request.user.seguindo.add(usuario_a_seguir)
    return redirect('perfil', usuario_id=usuario_id)

def deixar_seguir_usuario(request, usuario_id):
    usuario_a_deixar_de_seguir = get_object_or_404(Usuario, id=usuario_id)
    request.user.seguindo.remove(usuario_a_deixar_de_seguir)
    return redirect('perfil', usuario_id=usuario_id)