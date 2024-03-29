from django.shortcuts import render, redirect
from django.contrib import messages

def feed(request):
    user = request.user

    if not request.user.is_authenticated:
        messages.error(request, 'Usuário não logado')
        return redirect('login')
    
    return render(request, 'colecoes/feed.html', {'user': user})