from django.shortcuts import render, redirect
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

            nome = form.cleaned_data["nome_cadastro"]
            email = form.cleaned_data["email"]
            senha = form.cleaned_data["senha_1"]

            if Usuario.objects.filter(username=nome).exists():  # Altere esta linha
                messages.error(request, f'{nome} já existe!')
                return redirect('cadastro')

            usuario = Usuario.objects.create_user(  # Altere esta linha
                username=nome,
                email=email,
                password=senha
            )
            usuario.save()
            messages.success(request, f'{nome} cadastrado com sucesso!')
            return redirect('login')

    return render(request, "usuarios/cadastro.html", {"form": form})

def logout(request):
    auth.logout(request)
    messages.success(request, 'Logout efetuado com sucesso!')
    return redirect('login')